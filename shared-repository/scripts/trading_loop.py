#!/usr/bin/env python3
"""Trading Loop — Reads market intel pipeline, produces buy/sell/hold signals."""
import json, os, glob
from datetime import datetime, timezone

MARKET_DIR = os.environ.get("MARKET_INTEL_PATH", "/root/shared-repository/data/market-intel/raw/")
OUTPUT_DIR = os.environ.get("TRADING_OUTPUT_DIR", "/root/loop-logs")

CRYPTO_THRESHOLDS = {
    "strong_buy": -10.0,
    "buy": -5.0,
    "sell": 15.0,
    "strong_sell": 25.0,
}

STOCK_VOLUME_FLOOR = 100000
STOCK_PRICE_FLOOR = 1.00

def read_jsonl(path):
    entries = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    entries.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
    return entries

def analyse_crypto(entries):
    signals = []
    for entry in entries:
        if entry.get("source") != "coingecko":
            continue
        data = entry.get("data", [])
        coins = data if isinstance(data, list) else []
        for coin in coins:
            change = coin.get("change_24h_pct", coin.get("price_change_percentage_24h", 0))
            if change is None:
                continue
            change = float(change)
            name = coin.get("name", coin.get("symbol", "unknown"))
            price = coin.get("price_usd", coin.get("current_price", 0))
            
            signal = "HOLD"
            if change <= CRYPTO_THRESHOLDS["strong_buy"]:
                signal = "STRONG_BUY"
            elif change <= CRYPTO_THRESHOLDS["buy"]:
                signal = "BUY"
            elif change >= CRYPTO_THRESHOLDS["strong_sell"]:
                signal = "STRONG_SELL"
            elif change >= CRYPTO_THRESHOLDS["sell"]:
                signal = "SELL"
            
            if signal != "HOLD":
                signals.append({
                    "asset": name, "type": "crypto",
                    "price_usd": price, "change_24h": change, "signal": signal,
                })
    return signals

def analyse_stocks(entries):
    signals = []
    for entry in entries:
        if entry.get("source") != "alphavantage":
            continue
        data = entry.get("data", [])
        items = data if isinstance(data, list) else []
        for stock in items:
            ticker = stock.get("ticker", "")
            price = float(stock.get("price", 0))
            change_pct = stock.get("change_pct", stock.get("change_percentage", "0"))
            if isinstance(change_pct, str):
                change_pct = float(change_pct.replace("%", "").replace("+", ""))
            volume = int(stock.get("volume", 0))
            category = stock.get("category", "unknown")
            
            if volume < STOCK_VOLUME_FLOOR:
                continue
            if price < STOCK_PRICE_FLOOR:
                continue
            if ticker.endswith("W"):
                continue
            
            signals.append({
                "asset": ticker, "type": "stock",
                "price_usd": price, "change_pct": change_pct,
                "volume": volume, "category": category,
                "signal": "WATCH_GAINER" if "gainer" in category else "WATCH_LOSER",
            })
    return signals

def main():
    now = datetime.now(timezone.utc)
    date_str = now.strftime("%Y-%m-%d")
    
    all_entries = []
    for f in glob.glob(os.path.join(MARKET_DIR, f"*-{date_str}.jsonl")):
        all_entries.extend(read_jsonl(f))
    
    if not all_entries:
        print(f"No market data for {date_str}")
        return
    
    crypto_signals = analyse_crypto(all_entries)
    stock_signals = analyse_stocks(all_entries)
    all_signals = crypto_signals + stock_signals
    
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    out_path = os.path.join(OUTPUT_DIR, f"trading-loop-{date_str}.jsonl")
    with open(out_path, "a") as f:
        entry = {
            "loop_id": f"TRADE-{now.strftime('%Y%m%d%H%M')}",
            "loop_name": "trading-loop",
            "timestamp": now.isoformat(),
            "market_records_read": len(all_entries),
            "crypto_signals": len(crypto_signals),
            "stock_signals": len(stock_signals),
            "total_signals": len(all_signals),
            "signals": all_signals,
            "filters_applied": {
                "stock_volume_floor": STOCK_VOLUME_FLOOR,
                "stock_price_floor": STOCK_PRICE_FLOOR,
                "exclude_warrants": True,
            },
            "status": "DONE",
        }
        f.write(json.dumps(entry) + "\n")
    
    print(f"Trading loop: {len(all_signals)} signals ({len(crypto_signals)} crypto, {len(stock_signals)} stock)")
    for s in all_signals[:10]:
        print(f"  {s['signal']:14s} {s['asset']:20s} ${s.get('price_usd',0):>10.2f} ({s.get('change_24h', s.get('change_pct',0)):+.1f}%)")

if __name__ == "__main__":
    print(f"Trading Loop — {datetime.now(timezone.utc).isoformat()}")
    main()
