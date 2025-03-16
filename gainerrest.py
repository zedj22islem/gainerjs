import asyncio
import json
import time
from datetime import datetime
import telegram
import aiohttp
import os

# Configuration
TELEGRAM_BOT_TOKEN = "7669206577:AAFkCNJGkclyHf1w3x82DdLOAQDXUZ1Zzp4"
TELEGRAM_CHAT_ID = "5959819558"

MIN_VOLUME = 1800000
VOLUME_SURGE = 1.07
LOSER_RANGE = (-5.0, -1.0)
GAINER_RANGE = (1.0, 5.0)
TARGET_LOSER_GAIN = 4.0
TARGET_GAINER_GAIN = 6.5
MAX_GAIN = 50.0
CHECK_INTERVAL = 15
MIN_TREND_POINTS = 1
MIN_PRICE_INCREASE = 0.7
MAX_AGE = 86400

COINS = [
    '1000SATSUSDT', 'ACEUSDT', 'ACHUSDT', 'ACTUSDT', 'ACXUSDT', 'ADAUSDT', 'ADXUSDT', 'AERGOUSDT', 'AGLDUSDT', 'AIXBTUSDT',
    'ALGOUSDT', 'ALICEUSDT', 'ALPHAUSDT', 'AMBUSDT', 'ANKRUSDT', 'APEUSDT', 'API3USDT', 'APTUSDT', 'ARUSDT', 'ARKUSDT',
    'ARPAUSDT', 'ASTRUSDT', 'ATAUSDT', 'ATOMUSDT', 'AUDIOUSDT', 'AVAXUSDT', 'AXSUSDT', 'BAKEUSDT', 'BALUSDT', 'BANDUSDT',
    'BATUSDT', 'BCHUSDT', 'BELUSDT', 'BICOUSDT', 'BIGTIMEUSDT', 'BLUEBIRDUSDT', 'BLURUSDT', 'BLZUSDT', 'BNBUSDT', 'BNTUSDT',
    'BNXUSDT', 'BOMEUSDT', 'BONDUSDT', 'BRETTUSDT', 'BSVUSDT', 'BTCUSDT', 'C98USDT', 'CAKEUSDT', 'CANTOUSDT', 'CATIUSDT',
    'CELOUSDT', 'CELRUSDT', 'CFXUSDT', 'CHESSUSDT', 'CHRUSDT', 'CHZUSDT', 'CKBUSDT', 'COCOSOSDT', 'COMBOUSDT', 'COMPUSDT',
    'COREUSDT', 'COTIUSDT', 'CREAMUSDT', 'CROUSDT', 'CRVUSDT', 'CTKUSDT', 'CTSIUSDT', 'CVCUSDT', 'CYBERUSDT', 'DARUSDT',
    'DASHUSDT', 'DATAUSDT', 'DCRUSDT', 'DENTUSDT', 'DFUSDT', 'DGBUSDT', 'DODOUSDT', 'DOGEUSDT', 'DOTUSDT', 'DUSKUSDT',
    'DYDXUSDT', 'DYMUSDT', 'EDUUSDT', 'EGLDUSDT', 'ENJUSDT', 'ENSUSDT', 'EOSUSDT', 'ETCUSDT', 'ETHUSDT', 'ETHWUSDT',
    'FARMUSDT', 'FETUSDT', 'FIDAUSDT', 'FILUSDT', 'FIOUSDT', 'FLMUSDT', 'FLOKIUSDT', 'FLOWUSDT', 'FLUXUSDT', 'FORTHUSDT',
    'FRONTUSDT', 'FTMUSDT', 'FUNUSDT', 'FXSUSDT', 'GALAUSDT', 'GASUSDT', 'GFTUSDT', 'GLMRUSDT', 'GLMUSDT', 'GMTUSDT',
    'GNOUSDT', 'GNSUSDT', 'GODSUSDT', 'GPSUSDT', 'GRTUSDT', 'GTCUSDT', 'HBARUSDT', 'HFTUSDT', 'HIFIUSDT', 'HIGHUSDT',
    'HNTUSDT', 'HOTUSDT', 'ICPUSDT', 'ICXUSDT', 'IDEXUSDT', 'IDUSDT', 'ILVUSDT', 'IMXUSDT', 'INJUSDT', 'IOSTUSDT',
    'IOTAUSDT', 'IOTXUSDT', 'JASMYUSDT', 'JOEUSDT', 'JSTUSDT', 'KAVAUSDT', 'KDAUSDT', 'KLAYUSDT', 'KNCUSDT', 'KSMUSDT',
    'LDOUSDT', 'LEVERUSDT', 'LINAUSDT', 'LINKUSDT', 'LITUSDT', 'LPTUSDT', 'LQTYUSDT', 'LRCUSDT', 'LSKUSDT', 'LTCUSDT',
    'LTOUSDT', 'LUNA2USDT', 'LUNCUSDT', 'MAGICUSDT', 'MANAUSDT', 'MASKUSDT', 'MATICUSDT', 'MAVUSDT', 'MBOXUSDT', 'MDTUSDT',
    'MEMEUSDT', 'METISUSDT', 'MINAUSDT', 'MKRUSDT', 'MLNUSDT', 'MNTUSDT', 'MOVRUSDT', 'MTLUSDT', 'NEARUSDT', 'NEOUSDT',
    'NEXOUSDT', 'NFTUSDT', 'NKNUSDT', 'NMRUSDT', 'NOTUSDT', 'NTRNUSDT', 'OCEANUSDT', 'OGNUSDT', 'OMGUSDT', 'ONEUSDT',
    'ONTUSDT', 'OPUSDT', 'ORBSUSDT', 'ORDIUSDT', 'OXTUSDT', 'PAXGUSDT', 'PENDLEUSDT', 'PEOPLEUSDT', 'PERPUSDT', 'PHBUSDT',
    'PNTUSDT', 'POLSUSDT', 'PONDUSDT', 'PORTALUSDT', 'POWRUSDT', 'PROSUSDT', 'PUNDIXUSDT', 'PYRUSDT', 'QNTUSDT', 'QTUMUSDT',
    'RADUSDT', 'RAREUSDT', 'RAYUSDT', 'RDNTUSDT', 'REEFUSDT', 'RENUSDT', 'REQUSDT', 'RLCUSDT', 'RNDRUSDT', 'ROSEUSDT',
    'RSRUSDT', 'RUNEUSDT', 'RVNUSDT', 'SANDUSDT', 'SCUSDT', 'SEIUSDT', 'SFPUSDT', 'SHIBUSDT', 'SKLUSDT', 'SLPUSDT',
    'SNTUSDT', 'SNXUSDT', 'SOLUSDT', 'SPELLUSDT', 'SSVUSDT', 'STEEMUSDT', 'STGUSDT', 'STMXUSDT', 'STORJUSDT', 'STRAXUSDT',
    'STXUSDT', 'SUIUSDT', 'SUPERUSDT', 'SUSHIUSDT', 'SXPUSDT', 'THETAUSDT', 'TIAUSDT', 'TLMUSDT', 'TNSRUSDT', 'TOKENUSDT',
    'TRBUSDT', 'TRUUSDT', 'TRXUSDT', 'TWTUSDT', 'UMAUSDT', 'UNFIUSDT', 'UNIUSDT', 'USDCUSDT', 'USTCUSDT', 'VETUSDT',
    'VGXUSDT', 'VRAUSDT', 'VTHOUSDT', 'WAVESUSDT', 'WAXPUSDT', 'WLDUSDT', 'WOOUSDT', 'XAIUSDT', 'XCHUSDT', 'XEMUSDT',
    'XLMUSDT', 'XMRUSDT', 'XRPUSDT', 'XTZUSDT', 'XVGUSDT', 'XVSUSDT', 'YFIUSDT', 'YGGUSDT', 'ZECUSDT', 'ZENUSDT',
    'ZILUSDT', 'ZRXUSDT'
]

async def send_telegram_alert(bot, coin, price, percent_change, initial_change, volume, initial_volume, initial_price, trend_type, profit_target, entry_time, alert_count=0, last_price=0):
    volume_surge = (volume / initial_volume) * 100 - 100
    volume_increase = volume - initial_volume
    # Confidence based on volume surge (> 50%) and significant price movement (> 5% from initial)
    confidence = "High" if volume_surge > 50 and (percent_change - initial_change) > 5 else "Moderate" if volume_surge > 0 else "Low"
    transition_time = time.time() - entry_time
    hours, remainder = divmod(transition_time, 3600)
    minutes, seconds = divmod(remainder, 60)
    transition_str = f"{int(hours)}h {int(minutes)}m {int(seconds)}s"
    entry_time_str = datetime.fromtimestamp(entry_time).strftime('%H:%M:%S')
    alert_time_str = datetime.now().strftime('%H:%M:%S')
    coin_status = "✅ Coin exists in COINS list ✅" if coin in COINS else "❌ Coin does not exist in COINS list ❌"

    message = (
        f"🔥 *{coin} {trend_type}* 🚀\n"
        f"📊 *{percent_change:.2f}% Now (from {initial_change:.2f}%)* | Confidence: {confidence} 🎯\n"
        f"💰 Price: ${price:.4f} (Started at ${initial_price:.4f}" + (f", Last: ${last_price:.4f}" if last_price > 0 else "") + ") 📈\n"
        f"📊 24H Volume: ${volume:,.0f} (+${volume_increase:.0f}) 📈\n"
        f"📈 Vol Surge: {volume_surge:.0f}% 🚀\n"
        f"💸 Profit Target: ${profit_target:.4f} (20% gain) 🎯\n"
        f"⏰ Transition Time: {transition_str} ⏳\n"
        f"⏰ Entered: {entry_time_str} 📅\n"
        f"⏰ Alerted: {alert_time_str} 📅\n"
        f"🔔 Alerts Since Tracked: {alert_count} 🔄\n"
        f"{coin_status}"
    )
    
    await bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message, parse_mode='Markdown')
    print(f"Alert triggered for {coin} - Check Telegram!")

def is_uptrend(data_points):
    if len(data_points) < MIN_TREND_POINTS:
        return False
    changes = [d[1] for d in data_points]
    prices = [d[3] for d in data_points]
    for i in range(len(changes) - 1):
        if changes[i] >= changes[i + 1]:
            return False
        price_increase = ((prices[i + 1] - prices[i]) / prices[i]) * 100
        if price_increase < MIN_PRICE_INCREASE:
            return False
    return True

async def fetch_ticker_data():
    async with aiohttp.ClientSession() as session:
        async with session.get("https://api.binance.com/api/v3/ticker/24hr") as response:
            if response.status != 200:
                print(f"[{datetime.now().strftime('%H:%M:%S')}] API request failed with status {response.status}")
                return []
            return await response.json()

async def monitor_dynamic_pumps():
    if os.name == 'nt':
        loop = asyncio.SelectorEventLoop()
        asyncio.set_event_loop(loop)
    else:
        loop = asyncio.get_event_loop()

    print(f"Starting dynamic pump detector at {datetime.now().strftime('%H:%M:%S')} with loop: {loop.__class__.__name__}")
    bot = telegram.Bot(token=TELEGRAM_BOT_TOKEN)
    coin_data = {}
    already_alerted = {}
    last_check = 0
    retry_delay = 5

    try:
        while True:
            try:
                tickers = await fetch_ticker_data()
                if not tickers:
                    print(f"[{datetime.now().strftime('%H:%M:%S')}] Failed to fetch ticker data, retrying...")
                    await asyncio.sleep(retry_delay)
                    retry_delay = min(retry_delay * 2, 60)
                    continue
                
                retry_delay = 5
                current_time = time.time()
                
                # Clean up coin_data for coins not in latest tickers or not meeting MIN_VOLUME
                coin_data = {symbol: data for symbol, data in coin_data.items() if any(t['symbol'] == symbol for t in tickers) and data['history'][-1][2] >= MIN_VOLUME}
                
                for ticker in tickers:
                    symbol = ticker["symbol"]
                    if not symbol.endswith("USDT"):  # Only process USDT pairs
                        continue
                    percent_change = round(float(ticker["priceChangePercent"]), 2)
                    volume = float(ticker["quoteVolume"])
                    price = float(ticker["lastPrice"])
                    if volume < MIN_VOLUME:
                        continue
                    
                    if symbol not in coin_data and (LOSER_RANGE[0] <= percent_change <= LOSER_RANGE[1] or GAINER_RANGE[0] <= percent_change <= GAINER_RANGE[1]):
                        coin_data[symbol] = {
                            'entry_time': current_time,
                            'initial_change': percent_change,
                            'initial_volume': volume,
                            'initial_price': price,
                            'history': [(current_time, percent_change, volume, price)]
                        }
                        print(f"Added {symbol}: {percent_change:.2f}%, Vol: ${volume:,.0f}, Price: ${price:.4f} at {datetime.now().strftime('%H:%M:%S')}")
                    
                    elif symbol in coin_data:
                        data = coin_data[symbol]
                        data['history'].append((current_time, percent_change, volume, price))
                        if len(data['history']) > 10:
                            data['history'] = data['history'][-10:]
                
                if current_time - last_check >= CHECK_INTERVAL and (len(coin_data) > 0 or len(already_alerted) > 0):
                    last_check = current_time
                    to_remove = []
                    
                    for symbol, data in list(coin_data.items()):
                        ticker = next((t for t in tickers if t["symbol"] == symbol), None)
                        if not ticker or len(data['history']) < 2:
                            to_remove.append(symbol)
                            continue
                        price = float(ticker["lastPrice"])
                        percent_change = round(float(ticker["priceChangePercent"]), 2)
                        volume = float(ticker["quoteVolume"])
                        if volume < MIN_VOLUME or percent_change > MAX_GAIN:
                            to_remove.append(symbol)
                            continue
                        
                        initial_change = data['initial_change']
                        initial_volume = data['initial_volume']
                        initial_price = data['initial_price']
                        volume_surge = volume / initial_volume
                        profit_target = price * 1.2
                        uptrend = is_uptrend(data['history'][-MIN_TREND_POINTS:])
                        
                        if current_time - data['entry_time'] > MAX_AGE:
                            to_remove.append(symbol)
                            continue
                        
                        if (LOSER_RANGE[0] <= initial_change <= LOSER_RANGE[1] and
                            percent_change >= TARGET_LOSER_GAIN and
                            volume_surge >= VOLUME_SURGE and
                              symbol not in already_alerted):
                            print(f"[{datetime.now().strftime('%H:%M:%S')}] {symbol}: {percent_change:.2f}% (from {initial_change:.2f}%, Vol: ${volume:,.0f}, Surge: {volume_surge:.2f}x) - Loser to Gainer")
                            await send_telegram_alert(bot, symbol, price, percent_change, initial_change, volume, initial_volume, initial_price, "Loser to Gainer", profit_target, data['entry_time'])
                            already_alerted[symbol] = {
                                'entry_time': data['entry_time'],
                                'initial_change': data['initial_change'],
                                'initial_volume': data['initial_volume'],
                                'initial_price': data['initial_price'],
                                'last_price': price,
                                'last_volume': volume,
                                'alert_count': 1,
                                'history': data['history'][-10:]
                            }
                            to_remove.append(symbol)
                        
                        elif (GAINER_RANGE[0] <= initial_change <= GAINER_RANGE[1] and
                              percent_change >= TARGET_GAINER_GAIN and
                              volume_surge >= VOLUME_SURGE and
                                symbol not in already_alerted):
                            print(f"[{datetime.now().strftime('%H:%M:%S')}] {symbol}: {percent_change:.2f}% (from {initial_change:.2f}%, Vol: ${volume:,.0f}, Surge: {volume_surge:.2f}x) - Gainer Climbing")
                            await send_telegram_alert(bot, symbol, price, percent_change, initial_change, volume, initial_volume, initial_price, "Gainer Climbing", profit_target, data['entry_time'])
                            already_alerted[symbol] = {
                                'entry_time': data['entry_time'],
                                'initial_change': data['initial_change'],
                                'initial_volume': data['initial_volume'],
                                'initial_price': data['initial_price'],
                                'last_price': price,
                                'last_volume': volume,
                                'alert_count': 1,
                                'history': data['history'][-10:]
                            }
                            to_remove.append(symbol)
                    
                    for symbol in to_remove:
                        coin_data.pop(symbol, None)
                
                # Monitor already alerted coins
                for symbol, data in list(already_alerted.items()):
                    ticker = next((t for t in tickers if t["symbol"] == symbol), None)
                    if not ticker:
                        already_alerted.pop(symbol, None)
                        continue
                    current_price = float(ticker["lastPrice"])
                    current_volume = float(ticker["quoteVolume"])
                    # Calculate total percent change from initial_price
                    total_percent_change = ((current_price - data['initial_price']) / data['initial_price']) * 100 if data['initial_price'] > 0 else 0
                    # Calculate total volume change from initial_volume
                    total_volume_change_percent = ((current_volume - data['initial_volume']) / data['initial_volume']) * 100 if data['initial_volume'] > 0 else 0
                    # Calculate change since last alert
                    price_change_since_last = ((current_price - data['last_price']) / data['last_price']) * 100 if data['last_price'] > 0 else 0
                    volume_change_since_last = ((current_volume - data['last_volume']) / data['last_volume']) * 100 if data['last_volume'] > 0 else 0
                    
                    '''print(f"Debug - {symbol}: current_price={current_price}, initial_price={data['initial_price']}, "
                          f"current_volume={current_volume}, initial_volume={data['initial_volume']}, "
                          f"last_price={data['last_price']}, last_volume={data['last_volume']}, "
                          f"price_change_since_last={price_change_since_last:.2f}%, "
                          f"volume_change_since_last={volume_change_since_last:.2f}%")
                    '''
                    # Require positive price change and meet both 2% thresholds
                    if (price_change_since_last > 2.0 and volume_change_since_last > 2.0):
                        profit_target = current_price * 1.2
                        data['alert_count'] += 1
                        data['last_price'] = current_price
                        data['last_volume'] = current_volume
                        await send_telegram_alert(bot, symbol, current_price, total_percent_change, data['initial_change'], 
                                                 current_volume, data['initial_volume'], data['initial_price'], 
                                                 "Subsequent Gain", profit_target, data['entry_time'], data['alert_count'], data['last_price'])
                    
                    # Check for deletion conditions
                    if (current_time - data['entry_time'] > MAX_AGE or 
                        abs(((current_price - data['initial_price']) / data['initial_price']) * 100) > MAX_GAIN):
                        already_alerted.pop(symbol, None)
                        print(f"[{datetime.now().strftime('%H:%M:%S')}] Removed {symbol} from already_alerted (Max Age or Max Gain exceeded)")
                
                await asyncio.sleep(2)
            
            except Exception as e:
                print(f"[{datetime.now().strftime('%H:%M:%S')}] Error during ticker processing: {e}")
                await asyncio.sleep(retry_delay)
                retry_delay = min(retry_delay * 2, 60)
        
    except Exception as e:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Critical error: {e}")
    finally:
        loop.close()

if __name__ == "__main__":
    if os.name == 'nt':
        loop = asyncio.SelectorEventLoop()
        asyncio.set_event_loop(loop)
        print(f"Using event loop: {loop.__class__.__name__}")
    else:
        loop = asyncio.get_event_loop()
        print(f"Using event loop: {loop.__class__.__name__}")
    
    try:
        loop.run_until_complete(monitor_dynamic_pumps())
    except KeyboardInterrupt:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Script interrupted by user")
    except Exception as e:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Fatal error: {e}")
    finally:
        loop.close()









'''
import asyncio
import json
import time
from datetime import datetime
import telegram
import aiohttp
import os

# Configuration
TELEGRAM_BOT_TOKEN = "7669206577:AAFkCNJGkclyHf1w3x82DdLOAQDXUZ1Zzp4"
TELEGRAM_CHAT_ID = "5959819558"

MIN_VOLUME = 1800000
VOLUME_SURGE = 1.05
LOSER_RANGE = (-5.0, -1.0)
GAINER_RANGE = (1.0, 4.0)
TARGET_LOSER_GAIN = 3.0
TARGET_GAINER_GAIN = 5.5
MAX_GAIN = 50.0
CHECK_INTERVAL = 30
MIN_TREND_POINTS = 2
MIN_PRICE_INCREASE = 0.7
MAX_AGE = 86400

COINS = [
    '1000SATSUSDT', 'ACEUSDT', 'ACHUSDT', 'ACTUSDT', 'ACXUSDT', 'ADAUSDT', 'ADXUSDT', 'AERGOUSDT', 'AGLDUSDT', 'AIXBTUSDT',
    'ALGOUSDT', 'ALICEUSDT', 'ALPHAUSDT', 'AMBUSDT', 'ANKRUSDT', 'APEUSDT', 'API3USDT', 'APTUSDT', 'ARUSDT', 'ARKUSDT',
    'ARPAUSDT', 'ASTRUSDT', 'ATAUSDT', 'ATOMUSDT', 'AUDIOUSDT', 'AVAXUSDT', 'AXSUSDT', 'BAKEUSDT', 'BALUSDT', 'BANDUSDT',
    'BATUSDT', 'BCHUSDT', 'BELUSDT', 'BICOUSDT', 'BIGTIMEUSDT', 'BLUEBIRDUSDT', 'BLURUSDT', 'BLZUSDT', 'BNBUSDT', 'BNTUSDT',
    'BNXUSDT', 'BOMEUSDT', 'BONDUSDT', 'BRETTUSDT', 'BSVUSDT', 'BTCUSDT', 'C98USDT', 'CAKEUSDT', 'CANTOUSDT', 'CATIUSDT',
    'CELOUSDT', 'CELRUSDT', 'CFXUSDT', 'CHESSUSDT', 'CHRUSDT', 'CHZUSDT', 'CKBUSDT', 'COCOSUSDT', 'COMBOUSDT', 'COMPUSDT',
    'COREUSDT', 'COTIUSDT', 'CREAMUSDT', 'CROUSDT', 'CRVUSDT', 'CTKUSDT', 'CTSIUSDT', 'CVCUSDT', 'CYBERUSDT', 'DARUSDT',
    'DASHUSDT', 'DATAUSDT', 'DCRUSDT', 'DENTUSDT', 'DFUSDT', 'DGBUSDT', 'DODOUSDT', 'DOGEUSDT', 'DOTUSDT', 'DUSKUSDT',
    'DYDXUSDT', 'DYMUSDT', 'EDUUSDT', 'EGLDUSDT', 'ENJUSDT', 'ENSUSDT', 'EOSUSDT', 'ETCUSDT', 'ETHUSDT', 'ETHWUSDT',
    'FARMUSDT', 'FETUSDT', 'FIDAUSDT', 'FILUSDT', 'FIOUSDT', 'FLMUSDT', 'FLOKIUSDT', 'FLOWUSDT', 'FLUXUSDT', 'FORTHUSDT',
    'FRONTUSDT', 'FTMUSDT', 'FUNUSDT', 'FXSUSDT', 'GALAUSDT', 'GASUSDT', 'GFTUSDT', 'GLMRUSDT', 'GLMUSDT', 'GMTUSDT',
    'GNOUSDT', 'GNSUSDT', 'GODSUSDT', 'GPSUSDT', 'GRTUSDT', 'GTCUSDT', 'HBARUSDT', 'HFTUSDT', 'HIFIUSDT', 'HIGHUSDT',
    'HNTUSDT', 'HOTUSDT', 'ICPUSDT', 'ICXUSDT', 'IDEXUSDT', 'IDUSDT', 'ILVUSDT', 'IMXUSDT', 'INJUSDT', 'IOSTUSDT',
    'IOTAUSDT', 'IOTXUSDT', 'JASMYUSDT', 'JOEUSDT', 'JSTUSDT', 'KAVAUSDT', 'KDAUSDT', 'KLAYUSDT', 'KNCUSDT', 'KSMUSDT',
    'LDOUSDT', 'LEVERUSDT', 'LINAUSDT', 'LINKUSDT', 'LITUSDT', 'LPTUSDT', 'LQTYUSDT', 'LRCUSDT', 'LSKUSDT', 'LTCUSDT',
    'LTOUSDT', 'LUNA2USDT', 'LUNCUSDT', 'MAGICUSDT', 'MANAUSDT', 'MASKUSDT', 'MATICUSDT', 'MAVUSDT', 'MBOXUSDT', 'MDTUSDT',
    'MEMEUSDT', 'METISUSDT', 'MINAUSDT', 'MKRUSDT', 'MLNUSDT', 'MNTUSDT', 'MOVRUSDT', 'MTLUSDT', 'NEARUSDT', 'NEOUSDT',
    'NEXOUSDT', 'NFTUSDT', 'NKNUSDT', 'NMRUSDT', 'NOTUSDT', 'NTRNUSDT', 'OCEANUSDT', 'OGNUSDT', 'OMGUSDT', 'ONEUSDT',
    'ONTUSDT', 'OPUSDT', 'ORBSUSDT', 'ORDIUSDT', 'OXTUSDT', 'PAXGUSDT', 'PENDLEUSDT', 'PEOPLEUSDT', 'PERPUSDT', 'PHBUSDT',
    'PNTUSDT', 'POLSUSDT', 'PONDUSDT', 'PORTALUSDT', 'POWRUSDT', 'PROSUSDT', 'PUNDIXUSDT', 'PYRUSDT', 'QNTUSDT', 'QTUMUSDT',
    'RADUSDT', 'RAREUSDT', 'RAYUSDT', 'RDNTUSDT', 'REEFUSDT', 'RENUSDT', 'REQUSDT', 'RLCUSDT', 'RNDRUSDT', 'ROSEUSDT',
    'RSRUSDT', 'RUNEUSDT', 'RVNUSDT', 'SANDUSDT', 'SCUSDT', 'SEIUSDT', 'SFPUSDT', 'SHIBUSDT', 'SKLUSDT', 'SLPUSDT',
    'SNTUSDT', 'SNXUSDT', 'SOLUSDT', 'SPELLUSDT', 'SSVUSDT', 'STEEMUSDT', 'STGUSDT', 'STMXUSDT', 'STORJUSDT', 'STRAXUSDT',
    'STXUSDT', 'SUIUSDT', 'SUPERUSDT', 'SUSHIUSDT', 'SXPUSDT', 'THETAUSDT', 'TIAUSDT', 'TLMUSDT', 'TNSRUSDT', 'TOKENUSDT',
    'TRBUSDT', 'TRUUSDT', 'TRXUSDT', 'TWTUSDT', 'UMAUSDT', 'UNFIUSDT', 'UNIUSDT', 'USDCUSDT', 'USTCUSDT', 'VETUSDT',
    'VGXUSDT', 'VRAUSDT', 'VTHOUSDT', 'WAVESUSDT', 'WAXPUSDT', 'WLDUSDT', 'WOOUSDT', 'XAIUSDT', 'XCHUSDT', 'XEMUSDT',
    'XLMUSDT', 'XMRUSDT', 'XRPUSDT', 'XTZUSDT', 'XVGUSDT', 'XVSUSDT', 'YFIUSDT', 'YGGUSDT', 'ZECUSDT', 'ZENUSDT',
    'ZILUSDT', 'ZRXUSDT'
]

async def send_telegram_alert(bot, coin, price, percent_change, initial_change, volume, initial_volume, initial_price, trend_type, profit_target, entry_time):
    volume_surge = (volume / initial_volume) * 100 - 100
    volume_increase = volume - initial_volume
    confidence = "High" if volume_surge > 50 else "Moderate"
    transition_time = time.time() - entry_time
    hours, remainder = divmod(transition_time, 3600)
    minutes, seconds = divmod(remainder, 60)
    transition_str = f"{int(hours)}h {int(minutes)}m {int(seconds)}s"
    
    coin_status = "✅ Coin exists in COINS list ✅" if coin in COINS else "❌ Coin does not exist in COINS list ❌"
    
    message = (
        f"🔥 *{coin} {trend_type}* 🚀\n"
        f"📊 *{percent_change:.2f}% Now (from {initial_change:.2f}%)* | Confidence: {confidence} 🎯\n"
        f"💰 Price: ${price:.4f} (Started at ${initial_price:.4f}) 📈\n"
        f"📊 24H Volume: ${volume:,.0f} (+${volume_increase:.0f}) 📈\n"
        f"📈 Vol Surge: {volume_surge:.0f}% 🚀\n"
        f"💸 Profit Target: ${profit_target:.4f} (20% gain) 🎯\n"
        f"⏰ Transition Time: {transition_str} ⏳\n"
        f"⏰ Entered: {datetime.fromtimestamp(entry_time).strftime('%H:%M:%S')} 📅\n"
        f"⏰ Alerted: {datetime.now().strftime('%H:%M:%S')} 📅\n"
        f"{coin_status}"
    )
    await bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message, parse_mode='Markdown')
    print(f"Alert triggered for {coin} - Check Telegram!")

def is_uptrend(data_points):
    if len(data_points) < MIN_TREND_POINTS:
        return False
    changes = [d[1] for d in data_points]
    prices = [d[3] for d in data_points]
    for i in range(len(changes) - 1):
        if changes[i] >= changes[i + 1]:
            return False
        price_increase = ((prices[i + 1] - prices[i]) / prices[i]) * 100
        if price_increase < MIN_PRICE_INCREASE:
            return False
    return True

async def fetch_ticker_data():
    async with aiohttp.ClientSession() as session:
        async with session.get("https://api.binance.com/api/v3/ticker/24hr") as response:
            if response.status != 200:
                print(f"[{datetime.now().strftime('%H:%M:%S')}] API request failed with status {response.status}")
                return []
            return await response.json()

async def monitor_dynamic_pumps():
    # Explicitly set SelectorEventLoop on Windows for aiodns compatibility
    if os.name == 'nt':  # Check if running on Windows
        loop = asyncio.SelectorEventLoop()
        asyncio.set_event_loop(loop)
    else:
        loop = asyncio.get_event_loop()

    print(f"Starting dynamic pump detector at {datetime.now().strftime('%H:%M:%S')} with loop: {loop.__class__.__name__}")
    bot = telegram.Bot(token=TELEGRAM_BOT_TOKEN)
    coin_data = {}
    alerted_coins = set()
    last_check = 0
    retry_delay = 5  # Initial retry delay in seconds

    try:
        while True:
            try:
                tickers = await fetch_ticker_data()
                if not tickers:
                    print(f"[{datetime.now().strftime('%H:%M:%S')}] Failed to fetch ticker data, retrying...")
                    await asyncio.sleep(retry_delay)
                    retry_delay = min(retry_delay * 2, 60)  # Exponential backoff
                    continue
                
                retry_delay = 5  # Reset delay on successful fetch
                current_time = time.time()
                
                for ticker in tickers:
                    symbol = ticker["symbol"]
                    if not symbol.endswith("USDT"):
                        continue
                    percent_change = round(float(ticker["priceChangePercent"]), 2)
                    volume = float(ticker["quoteVolume"])
                    price = float(ticker["lastPrice"])
                    if volume < MIN_VOLUME:
                        continue
                    
                    if symbol not in coin_data and (LOSER_RANGE[0] <= percent_change <= LOSER_RANGE[1] or GAINER_RANGE[0] <= percent_change <= GAINER_RANGE[1]):
                        coin_data[symbol] = {
                            'entry_time': current_time,
                            'initial_change': percent_change,
                            'initial_volume': volume,
                            'initial_price': price,
                            'history': [(current_time, percent_change, volume, price)]
                        }
                        print(f"Added {symbol}: {percent_change:.2f}%, Vol: ${volume:,.0f}, Price: ${price:.4f} at {datetime.now().strftime('%H:%M:%S')}")
                        #print(f"Raw ticker for {symbol}: {ticker}")
                    
                    elif symbol in coin_data:
                        data = coin_data[symbol]
                        data['history'].append((current_time, percent_change, volume, price))
                        if len(data['history']) > 10:  # Prune history to save memory
                            data['history'] = data['history'][-10:]
                
                if current_time - last_check >= CHECK_INTERVAL and len(coin_data) > 0:
                    last_check = current_time
                    to_remove = []
                    
                    for symbol, data in list(coin_data.items()):
                        ticker = next((t for t in tickers if t["symbol"] == symbol), None)
                        if not ticker or len(data['history']) < 2:
                            continue
                        price = float(ticker["lastPrice"])
                        percent_change = round(float(ticker["priceChangePercent"]), 2)
                        volume = float(ticker["quoteVolume"])
                        if volume < MIN_VOLUME or percent_change > MAX_GAIN:
                            to_remove.append(symbol)
                            continue
                        
                        initial_change = data['initial_change']
                        initial_volume = data['initial_volume']
                        initial_price = data['initial_price']
                        volume_surge = volume / initial_volume
                        profit_target = price * 1.2
                        uptrend = is_uptrend(data['history'][-MIN_TREND_POINTS:])
                        
                        if current_time - data['entry_time'] > MAX_AGE:
                            to_remove.append(symbol)
                            continue
                        
                        if (LOSER_RANGE[0] <= initial_change <= LOSER_RANGE[1] and
                            percent_change >= TARGET_LOSER_GAIN and
                            volume_surge >= VOLUME_SURGE and
                            uptrend and symbol not in alerted_coins):
                            print(f"[{datetime.now().strftime('%H:%M:%S')}] {symbol}: {percent_change:.2f}% (from {initial_change:.2f}%, Vol: ${volume:,.0f}, Surge: {volume_surge:.2f}x) - Loser to Gainer")
                            await send_telegram_alert(bot, symbol, price, percent_change, initial_change, volume, initial_volume, initial_price, "Loser to Gainer", profit_target, data['entry_time'])
                            alerted_coins.add(symbol)
                            to_remove.append(symbol)
                        
                        elif (GAINER_RANGE[0] <= initial_change <= GAINER_RANGE[1] and
                              percent_change >= TARGET_GAINER_GAIN and
                              volume_surge >= VOLUME_SURGE and
                              uptrend and symbol not in alerted_coins):
                            print(f"[{datetime.now().strftime('%H:%M:%S')}] {symbol}: {percent_change:.2f}% (from {initial_change:.2f}%, Vol: ${volume:,.0f}, Surge: {volume_surge:.2f}x) - Gainer Climbing")
                            await send_telegram_alert(bot, symbol, price, percent_change, initial_change, volume, initial_volume, initial_price, "Gainer Climbing", profit_target, data['entry_time'])
                            alerted_coins.add(symbol)
                            to_remove.append(symbol)
                    
                    for symbol in to_remove:
                        coin_data.pop(symbol, None)
                
                await asyncio.sleep(2)  # Poll every 2 seconds to reduce load
            
            except Exception as e:
                print(f"[{datetime.now().strftime('%H:%M:%S')}] Error during ticker processing: {e}")
                await asyncio.sleep(retry_delay)
                retry_delay = min(retry_delay * 2, 60)
        
    except Exception as e:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Critical error: {e}")
    finally:
        loop.close()

if __name__ == "__main__":
    if os.name == 'nt':  # Ensure SelectorEventLoop is used on Windows
        loop = asyncio.SelectorEventLoop()
        asyncio.set_event_loop(loop)
        print(f"Using event loop: {loop.__class__.__name__}")
    else:
        loop = asyncio.get_event_loop()
        print(f"Using event loop: {loop.__class__.__name__}")
    
    try:
        loop.run_until_complete(monitor_dynamic_pumps())
    except KeyboardInterrupt:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Script interrupted by user")
    except Exception as e:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Fatal error: {e}")
    finally:
        loop.close()

'''