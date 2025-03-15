const fetch = require('node-fetch');
const TelegramBot = require('node-telegram-bot-api');

// Configuration
const TELEGRAM_BOT_TOKEN = '7669206577:AAFkCNJGkclyHf1w3x82DdLOAQDXUZ1Zzp4';
const TELEGRAM_CHAT_ID = '5959819558';

const MIN_VOLUME = 1800000;
const VOLUME_SURGE = 1.05;
const LOSER_RANGE = [-5.0, -1.0];
const GAINER_RANGE = [1.0, 4.0];
const TARGET_LOSER_GAIN = 3.0;
const TARGET_GAINER_GAIN = 5.5;
const MAX_GAIN = 50.0;
const CHECK_INTERVAL = 30 * 1000; // 30 seconds in milliseconds
const MIN_TREND_POINTS = 2;
const MIN_PRICE_INCREASE = 0.7;
const MAX_AGE = 86400 * 1000; // 24 hours in milliseconds

const COINS = [
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
];

async function sendTelegramAlert(bot, coin, price, percentChange, initialChange, volume, initialVolume, initialPrice, trendType, profitTarget, entryTime, alertCount = 0, lastPrice = 0) {
    const volumeSurge = (volume / initialVolume * 100) - 100;
    const volumeIncrease = volume - initialVolume;
    const confidence = volumeSurge > 50 && (percentChange - initialChange) > 5 ? 'High' : volumeSurge > 0 ? 'Moderate' : 'Low';
    const transitionTime = Date.now() - entryTime;
    const hours = Math.floor(transitionTime / 3600000);
    const remainder = transitionTime % 3600000;
    const minutes = Math.floor(remainder / 60000);
    const seconds = Math.floor((remainder % 60000) / 1000);
    const transitionStr = `${hours}h ${minutes}m ${seconds}s`;
    const entryTimeStr = new Date(entryTime).toLocaleTimeString('en-US', { hour12: false, hour: '2-digit', minute: '2-digit', second: '2-digit' });
    const alertTimeStr = new Date().toLocaleTimeString('en-US', { hour12: false, hour: '2-digit', minute: '2-digit', second: '2-digit' });
    const coinStatus = COINS.includes(coin) ? 'Coin exists in COINS list' : 'Coin does not exist in COINS list';

    const message = (
        `*${coin} ${trendType}*\n` +
        `Change: *${percentChange.toFixed(2)}% Now (from ${initialChange.toFixed(2)}%)* | Confidence: ${confidence}\n` +
        `Price: $${price.toFixed(4)} (Started at $${initialPrice.toFixed(4)}${lastPrice > 0 ? `, Last: $${lastPrice.toFixed(4)}` : ''})\n` +
        `24H Volume: $${volume.toLocaleString()} (+$${volumeIncrease.toLocaleString()})\n` +
        `Vol Surge: ${volumeSurge.toFixed(0)}%\n` +
        `Profit Target: $${profitTarget.toFixed(4)} (20% gain)\n` +
        `Transition Time: ${transitionStr}\n` +
        `Entered: ${entryTimeStr}\n` +
        `Alerted: ${alertTimeStr}\n` +
        `Alerts Since Tracked: ${alertCount}\n` +
        `${coinStatus}`
    );

    await bot.sendMessage(TELEGRAM_CHAT_ID, message, { parse_mode: 'Markdown' });
    console.log(`Alert triggered for ${coin} - Check Telegram!`);
}

function isUptrend(dataPoints) {
    if (dataPoints.length < MIN_TREND_POINTS) return false;
    const changes = dataPoints.map(d => d[1]);
    const prices = dataPoints.map(d => d[3]);
    for (let i = 0; i < changes.length - 1; i++) {
        if (changes[i] >= changes[i + 1]) return false;
        const priceIncrease = ((prices[i + 1] - prices[i]) / prices[i]) * 100;
        if (priceIncrease < MIN_PRICE_INCREASE) return false;
    }
    return true;
}

async function fetchTickerData() {
    try {
        const response = await fetch('https://api.binance.com/api/v3/ticker/24hr');
        if (response.status !== 200) {
            console.log(`[${new Date().toLocaleTimeString('en-US', { hour12: false, hour: '2-digit', minute: '2-digit', second: '2-digit' })}] API request failed with status ${response.status}`);
            return [];
        }
        const data = await response.json();
        return data.sort((a, b) => a.symbol.localeCompare(b.symbol));
    } catch (error) {
        console.log(`[${new Date().toLocaleTimeString('en-US', { hour12: false, hour: '2-digit', minute: '2-digit', second: '2-digit' })}] Error fetching ticker data: ${error.message}`);
        return [];
    }
}

async function monitorDynamicPumps() {
    console.log(`Starting dynamic pump detector at ${new Date().toLocaleTimeString('en-US', { hour12: false, hour: '2-digit', minute: '2-digit', second: '2-digit' })} with process: ${process.title}`);
    const bot = new TelegramBot(TELEGRAM_BOT_TOKEN, { polling: false });
    let coinData = {};
    let alreadyAlerted = {};
    let lastCheck = 0;
    let lastFetchTime = 0;
    let retryDelay = 5000; // 5 seconds in milliseconds
    let bufferedTickers = [];

    async function processTickers() {
        const currentTime = Date.now();
        if (currentTime - lastFetchTime >= 2000) { // Fetch every 2 seconds
            bufferedTickers = await fetchTickerData();
            lastFetchTime = currentTime;
            if (bufferedTickers.length === 0) {
                console.log(`[${new Date().toLocaleTimeString('en-US', { hour12: false, hour: '2-digit', minute: '2-digit', second: '2-digit' })}] Failed to fetch ticker data, retrying...`);
                return;
            }
            retryDelay = 5000;
        }

        // Clean up coinData for coins not in latest tickers or not meeting MIN_VOLUME
        coinData = Object.fromEntries(
            Object.entries(coinData).filter(([symbol, data]) =>
                bufferedTickers.some(t => t.symbol === symbol) && data.history[data.history.length - 1][2] >= MIN_VOLUME
            )
        );

        for (const ticker of bufferedTickers) {
            const symbol = ticker.symbol;
            if (!symbol.endsWith('USDT')) continue;
            const percentChange = Math.round(parseFloat(ticker.priceChangePercent) * 100) / 100;
            const volume = parseFloat(ticker.quoteVolume);
            const price = parseFloat(ticker.lastPrice);
            if (volume < MIN_VOLUME) continue;

            if (!coinData[symbol] &&
                ((percentChange >= LOSER_RANGE[0] && percentChange <= LOSER_RANGE[1]) ||
                    (percentChange >= GAINER_RANGE[0] && percentChange <= GAINER_RANGE[1]))) {
                coinData[symbol] = {
                    entryTime: currentTime,
                    initialChange: percentChange,
                    initialVolume: volume,
                    initialPrice: price,
                    history: [[currentTime, percentChange, volume, price]]
                };
                console.log(`Added ${symbol}: ${percentChange.toFixed(2)}%, Vol: $${volume.toLocaleString()}, Price: $${price.toFixed(4)} at ${new Date().toLocaleTimeString('en-US', { hour12: false, hour: '2-digit', minute: '2-digit', second: '2-digit' })}`);
            } else if (coinData[symbol]) {
                const data = coinData[symbol];
                data.history.push([currentTime, percentChange, volume, price]);
                if (data.history.length > 10) data.history = data.history.slice(-10);
            }
        }

        if (currentTime - lastCheck >= CHECK_INTERVAL && (Object.keys(coinData).length > 0 || Object.keys(alreadyAlerted).length > 0)) {
            lastCheck = currentTime;
            const toRemove = [];

            for (const [symbol, data] of Object.entries(coinData)) {
                const ticker = bufferedTickers.find(t => t.symbol === symbol);
                if (!ticker || data.history.length < 2) {
                    toRemove.push(symbol);
                    continue;
                }
                const price = parseFloat(ticker.lastPrice);
                const percentChange = Math.round(parseFloat(ticker.priceChangePercent) * 100) / 100;
                const volume = parseFloat(ticker.quoteVolume);
                if (volume < MIN_VOLUME || percentChange > MAX_GAIN) {
                    toRemove.push(symbol);
                    continue;
                }

                const initialChange = data.initialChange;
                const initialVolume = data.initialVolume;
                const initialPrice = data.initialPrice;
                const volumeSurge = volume / initialVolume;
                const profitTarget = price * 1.2;
                const uptrend = isUptrend(data.history.slice(-MIN_TREND_POINTS));

                if (currentTime - data.entryTime > MAX_AGE) {
                    toRemove.push(symbol);
                    continue;
                }

                if (initialChange >= LOSER_RANGE[0] && initialChange <= LOSER_RANGE[1] &&
                    percentChange >= TARGET_LOSER_GAIN && volumeSurge >= VOLUME_SURGE &&
                    uptrend && !alreadyAlerted[symbol]) {
                    console.log(`[${new Date().toLocaleTimeString('en-US', { hour12: false, hour: '2-digit', minute: '2-digit', second: '2-digit' })}] ${symbol}: ${percentChange.toFixed(2)}% (from ${initialChange.toFixed(2)}%, Vol: $${volume.toLocaleString()}, Surge: ${volumeSurge.toFixed(2)}x) - Loser to Gainer`);
                    await sendTelegramAlert(bot, symbol, price, percentChange, initialChange, volume, initialVolume, initialPrice, 'Loser to Gainer', profitTarget, data.entryTime);
                    alreadyAlerted[symbol] = {
                        entryTime: data.entryTime,
                        initialChange: data.initialChange,
                        initialVolume: data.initialVolume,
                        initialPrice: data.initialPrice,
                        lastPrice: price,
                        lastVolume: volume,
                        alertCount: 1,
                        history: data.history.slice(-10)
                    };
                    toRemove.push(symbol);
                } else if (initialChange >= GAINER_RANGE[0] && initialChange <= GAINER_RANGE[1] &&
                    percentChange >= TARGET_GAINER_GAIN && volumeSurge >= VOLUME_SURGE &&
                    uptrend && !alreadyAlerted[symbol]) {
                    console.log(`[${new Date().toLocaleTimeString('en-US', { hour12: false, hour: '2-digit', minute: '2-digit', second: '2-digit' })}] ${symbol}: ${percentChange.toFixed(2)}% (from ${initialChange.toFixed(2)}%, Vol: $${volume.toLocaleString()}, Surge: ${volumeSurge.toFixed(2)}x) - Gainer Climbing`);
                    await sendTelegramAlert(bot, symbol, price, percentChange, initialChange, volume, initialVolume, initialPrice, 'Gainer Climbing', profitTarget, data.entryTime);
                    alreadyAlerted[symbol] = {
                        entryTime: data.entryTime,
                        initialChange: data.initialChange,
                        initialVolume: data.initialVolume,
                        initialPrice: data.initialPrice,
                        lastPrice: price,
                        lastVolume: volume,
                        alertCount: 1,
                        history: data.history.slice(-10)
                    };
                    toRemove.push(symbol);
                }
            }

            for (const symbol of toRemove) {
                delete coinData[symbol];
            }

            // Monitor already alerted coins
            for (const [symbol, data] of Object.entries(alreadyAlerted)) {
                const ticker = bufferedTickers.find(t => t.symbol === symbol);
                if (!ticker) {
                    delete alreadyAlerted[symbol];
                    continue;
                }
                const currentPrice = parseFloat(ticker.lastPrice);
                const currentVolume = parseFloat(ticker.quoteVolume);
                const totalPercentChange = ((currentPrice - data.initialPrice) / data.initialPrice) * 100 || 0;
                const totalVolumeChangePercent = ((currentVolume - data.initialVolume) / data.initialVolume) * 100 || 0;
                const priceChangeSinceLast = ((currentPrice - data.lastPrice) / data.lastPrice) * 100 || 0;
                const volumeChangeSinceLast = ((currentVolume - data.lastVolume) / data.lastVolume) * 100 || 0;

                if (priceChangeSinceLast > 2.0 && volumeChangeSinceLast > 2.0) {
                    const profitTarget = currentPrice * 1.2;
                    data.alertCount += 1;
                    data.lastPrice = currentPrice;
                    data.lastVolume = currentVolume;
                    await sendTelegramAlert(bot, symbol, currentPrice, totalPercentChange, data.initialChange, currentVolume, data.initialVolume, data.initialPrice, 'Subsequent Gain', profitTarget, data.entryTime, data.alertCount, data.lastPrice);
                }

                if (currentTime - data.entryTime > MAX_AGE || Math.abs(((currentPrice - data.initialPrice) / data.initialPrice) * 100) > MAX_GAIN) {
                    delete alreadyAlerted[symbol];
                    console.log(`[${new Date().toLocaleTimeString('en-US', { hour12: false, hour: '2-digit', minute: '2-digit', second: '2-digit' })}] Removed ${symbol} from alreadyAlerted (Max Age or Max Gain exceeded)`);
                }
            }
        }
    }

    while (true) {
        try {
            await processTickers();
        } catch (error) {
            console.log(`[${new Date().toLocaleTimeString('en-US', { hour12: false, hour: '2-digit', minute: '2-digit', second: '2-digit' })}] Error during ticker processing: ${error.message}`);
            await new Promise(resolve => setTimeout(resolve, retryDelay));
            retryDelay = Math.min(retryDelay * 2, 60000);
        }
    }
}

if (require.main === module) {
    console.log(`Using process: ${process.title}`);
    monitorDynamicPumps().catch(err => console.error(`[${new Date().toLocaleTimeString('en-US', { hour12: false, hour: '2-digit', minute: '2-digit', second: '2-digit' })}] Fatal error: ${err.message}`));
}