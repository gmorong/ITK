import asyncio
import aiohttp
import json
from pathlib import Path


async def fetch_urls(input_file: str, output_file: str = None):
    input_path = Path(input_file)
    if output_file is None:
        output_file = input_path.parent / "results_2.jsonl"
    else:
        output_file = Path(output_file)
        
    output_file.parent.mkdir(parents=True, exist_ok=True)
    semaphore = asyncio.Semaphore(5)
    
    async def fetch_json(session: aiohttp.ClientSession, url: str):
        async with semaphore:
            try:
                async with session.get(
                    url,
                    timeout=aiohttp.ClientTimeout(total=300)
                ) as response:
                    if response.status != 200:
                        print(f"|ПРОПУСК| {url} --- статус: {response.status}")
                        return None
                    content = await response.text()
                    try:
                        json_data = json.loads(content)
                    except json.JSONDecodeError as e:
                        print(f"|ОШИБКА| {url} --- {e}")
                        return None
                    print(f"|ОК| {url}")
                    return {
                        "url": url,
                        "content": json_data
                    }
            except aiohttp.ClientError as e:
                print(f"|ОШИБКА| {url} --- {e}")
                return None
            except asyncio.TimeoutError:
                print(f"|ОШИБКА| {url} --- Таймаут")
                return None
            except Exception as e:
                print(f"|ОШИБКА| {url} --- {e}")
                return None
            
    connector = aiohttp.TCPConnector(ssl=False)
    async with aiohttp.ClientSession(connector=connector) as session:
        with open(output_file, 'w', encoding='utf-8') as out_f:
            batch = []
            batch_size = 50
            
            with open(input_file, 'r', encoding='utf-8') as in_f:
                for line in in_f:
                    url = line.strip()
                    if not url:
                        continue
                    
                    batch.append(url)
                    
                    if len(batch) >= batch_size:
                        print(f"")
                        tasks = [fetch_json(session, url) for url in batch]
                        results = await asyncio.gather(*tasks)
                        
                        for result in results:
                            if result:
                                line = json.dumps(result, ensure_ascii=False)
                                out_f.write(line + '\n')
                                out_f.flush()
                        batch = []
                if batch:
                    print(f"")
                    tasks = [fetch_json(session, url) for url in batch]
                    results = await asyncio.gather(*tasks)
                    
                    for result in results:
                        if result:
                            line = json.dumps(result, ensure_ascii=False)
                            out_f.write(line + '\n')
                            out_f.flush()
    print(f"|ЗАВЕРШЕНИЕ| Рез-ты сохранены в {output_file}")
    
    
if __name__ == '__main__':
    script_dir = Path(__file__).parent
    urls_file = script_dir / 'urls.txt'
    asyncio.run(fetch_urls(str(urls_file)))