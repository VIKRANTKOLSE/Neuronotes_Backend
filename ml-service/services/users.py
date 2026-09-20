from fastapi import FastAPI
import numpy as np
import logging
from config.database import app


class UserNotFoundError(Exception):
    """Raised when a userid does not exist in the users table."""
    def __init__(self, userid: int):
        self.userid = userid
        super().__init__(f"No user found with userid={userid}")


async def get_theta(app:FastAPI,userid: int) -> list[float]:
    pool = app.state.pool
    try:
        async with pool.connection() as conn:
            result = await conn.execute(
                "SELECT theta FROM users WHERE userid = %s",
                (userid,)
            )
            row = await result.fetchone()

            if row is None:
                logging.warning("User not found: userid=%s", userid)
                raise UserNotFoundError(userid)

            logging.info("Retrieved theta for userid=%s", userid)
            return row[0]

    except UserNotFoundError:
        raise
    except Exception as e:
        logging.error("Failed to fetch theta for userid=%s: %s", userid, str(e))
        raise RuntimeError(f"Database error while fetching theta for userid={userid}") from e


async def update_theta(
    app: FastAPI,
    user_id: int,
    quest_id: int,
    user_answer: int,
    predicted_prob: float,
    current_theta: np.ndarray
):
    pool = app.state.pool
    try:
        async with pool.connection() as conn:
            # Fetch correct_option and a_vector for this question
            result = await conn.execute(
                "SELECT correct_option, a_vector FROM questions WHERE quest_id = %s",
                (quest_id,)
            )
            row = await result.fetchone()

            if row is None:
                logging.error("Question not found: quest_id=%s", quest_id)
                raise ValueError(f"No question found with quest_id={quest_id}")

            correct_option = row[0]
            a_vector = np.array(row[1])

            # Binary correctness: 1 if correct, 0 if wrong
            X = 1 if user_answer == correct_option else 0

            # Error gradient and theta update
            error = X - predicted_prob
            eta = 0.1
            delta_theta = eta * error * a_vector
            new_theta = current_theta + delta_theta

            # Persist updated theta (convert to Python list for DOUBLE PRECISION[])
            await conn.execute(
                "UPDATE users SET theta = %s WHERE userid = %s",
                (new_theta.tolist(), user_id)
            )
            await conn.commit()

            logging.info(
                "Updated theta for userid=%s (quest_id=%s, correct=%s, error=%.4f)",
                user_id, quest_id, X, error
            )
            return new_theta

    except ValueError:
        raise
    except Exception as e:
        logging.error("Failed to update theta for userid=%s: %s", user_id, str(e))
        raise RuntimeError(f"Database error while updating theta for userid={user_id}") from e