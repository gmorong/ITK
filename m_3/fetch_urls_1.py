import asyncio
import aiohttp
import json
from pathlib import Path

urls = [
    "https://github.com/gmorong/ITK",
    "https://app.itk.academy/courses/1123",
    "https://app.todoist.com/app/todayl"
]


async def fetch_urls(urls: list[str], file_path: str):
    semaphore = asyncio.Semaphore(5)
    
    async def fetch_one(session: aiohttp.ClientSession, url: str) -> tuple[str, int]:
        async with semaphore:
            try:
                async with session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as response:
                    status = response.status
                    print(f"{url} --- {status}")
                    return url, status
            except aiohttp.ClientError as e:
                print(f"{url} --- ОШИБКА ПОДКЛЮЧЕНИЯ: {e}")
                return url, 0
            except asyncio.TimeoutError:
                print(f"{url} --- ТАЙМАУТ")
                return url, 0
            except Exception as e:
                print(f"{url} --- НЕИЗВЕСТНАЯ ОШИБКА: {e}")
                return url, 0
    
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_one(session, url) for url in urls]
        resposes = await asyncio.gather(*tasks)
        results = dict(resposes)
        
    with open(file_path, 'w', encoding='utf-8') as f:
        for url, status_code in results.items():
            line = json.dumps({"url": url, "status_code": status_code}, ensure_ascii=False)
            f.write(line + "\n")
            
    print(f"Результаты сохранены в {file_path}")
    return results
        


if __name__ == '__main__':
    script_dir = Path(__file__).parent
    output_file = script_dir / "results_1.jsonl"
    results = asyncio.run(fetch_urls(urls, str(output_file)))
    print("\nРезультаты:")
    for url, status in results.items():
        print(f"__{url}: {status}")