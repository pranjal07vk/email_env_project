import asyncio
from env import EmailEnv
from models import predict

async def test_env(n=20):
    total = 0

    for i in range(n):
        env = EmailEnv()
        result = await env.reset()

        action = predict(result.observation)
        result = await env.step(action)

        total += result.reward
        print(f"Test {i+1}: reward = {result.reward}")

    print(f"\nAverage Score: {total/n:.2f}")

if __name__ == "__main__":
    asyncio.run(test_env())