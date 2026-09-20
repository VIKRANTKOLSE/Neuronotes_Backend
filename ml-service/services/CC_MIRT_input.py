
import numpy as np
import logging
async def build_q_matrix(app):
    pool=app.state.pool
    if pool is not None:
        async with pool.connection() as conn:
            result = await conn.execute(
                "SELECT quest_id,a_vector,d_param from questions"
            )
            rows=await result.fetchall()
            quest_ids = [row[0] for row in rows]
            a_vectors = [row[1] for row in rows] 
            d_params = [row[2] for row in rows]
            

            app.state.quest_ids=np.array(quest_ids)
            app.state.q_matrix=np.array(a_vectors)
            app.state.d_params=np.array(d_params)

            logging.info(f"Loaded Q-Matrix into RAM. Shaoe: {app.state.q_matrix.shape}")

