
from fastapi import FastAPI
import numpy as np
import math
import logging

async def probability(app:FastAPI,j:int,userId:int,theta: np.ndarray):
    try:
        
        discrimination_vector=app.state.q_matrix[j-1]
        d_param=app.state.d_params[j-1]
        y = np.dot(discrimination_vector, theta) + d_param
        p=0.25+0.75*(1/(1+math.exp(-y)))
        return p
    except ZeroDivisionError:
        logging.error("ZeroDivisionError in probability: y=%s for userId=%s, questionIndex=%s", y, userId, j)
        raise ValueError(f"Math error computing probability for userId={userId}, questionIndex={j}")
    except Exception as e:
        logging.error("Failed to compute probability for userId=%s, questionIndex=%s: %s", userId, j, str(e))
        raise


async def adaptive_selection(app,userid: int,theta: np.ndarray) -> int:
    all_quest_ids = app.state.quest_ids
    q_matrix = app.state.q_matrix
    d_params = app.state.d_params

    # Fetch already-answered question IDs for this user from submissions
    pool = app.state.pool
    async with pool.connection() as conn:
        result = await conn.execute(
            """
            SELECT s.questid
            FROM submissions AS s
            JOIN questions AS q ON q.quest_id = s.questid
            WHERE s.userid = %s
            """,
            (userid,)
        )
        rows = await result.fetchall()
    answered_quest_ids = [row[0] for row in rows]

    # Boolean mask: True for questions NOT yet answered
    answered_mask = np.isin(all_quest_ids, answered_quest_ids)
    valid_mask = ~answered_mask

    valid_quest_ids = all_quest_ids[valid_mask]

    if valid_quest_ids.size == 0:
        raise ValueError("No unanswered questions remaining in the item bank")

    A_valid = q_matrix[valid_mask]
    D_valid = d_params[valid_mask]

    # Batch logits: Y = A_valid · user_theta + D_valid
    Y = np.dot(A_valid, theta) + D_valid

    # Batch probability with 25% guessing floor: P = 0.25 + 0.75 * sigmoid(Y)
    P = 0.25 + 0.75 * (1.0 / (1.0 + np.exp(-Y)))

    # Item information: I_KL = ||a_j||^2 * P * (1 - P)
    discrimination = np.sum(A_valid ** 2, axis=1)
    I_KL = discrimination * P * (1.0 - P)

    # Select the question with maximum information
    best_idx = np.argmax(I_KL)

    return int(valid_quest_ids[best_idx])
