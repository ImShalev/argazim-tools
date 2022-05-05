import web3
from keep_alive import keep_alive
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from replit import db
import discord
import requests
import os
import datetime

# secrets
token = os.environ.get("bot_token")
blocknative_api = os.environ.get("blocknative")
etherscan_api = os.environ.get("etherscan")
ethplorer_api = os.environ.get("ethplorer")

# discord ids
shalev_id = 212661493034909696
naor_id = 270174990429716480
erez_id = 176647476365754368
channel_joiner_id = 946588591390355546
channel_links_id = 946910748607660093
channel_spam_id = 948327123322552441
channel_sunspot_id = 944701722058719272

w3 = web3.Web3(web3.HTTPProvider('https://eth-mainnet.alchemyapi.io/v2/VuG8kJk3PpUQmg7_wcVt0wzJwsa5E2U6'))

# bind client as a discord client
client = discord.Client()

# when bot goes online
@client.event
async def on_ready():
	await client.get_channel(channel_spam_id).send("🟢 Argazim Tools is online!")

# when someone sends a message
@client.event
async def on_message(message):
	if message.author == client.user: return

	if message.author.id == erez_id and db['whale']:
		await message.reply("https://tenor.com/view/whale-hellothere-hello-hi-hey-gif-4505186")
	
	if message.content.startswith("!"):
		embed = discord.Embed(color=0xE78E5A)
		embed.set_footer(text="Argazim Tools", icon_url="https://i.imgur.com/8YqUQNL.png")
		command = message.content[1:].split()[0].lower()
		parameters = message.content[1:].split()[1:]
		if command == 'help':
			await help(message, command, parameters, embed)
		elif command == 'ping':
			await message.reply('pong')
		elif command == 'gas':
			await gas(message, command, parameters, embed)
		elif command in ('eth', 'price'):
			await binance(message, command, parameters, embed)
		elif command in ('floor', 'royalty'):
			await nft_metrics(message, command, parameters, embed)
		elif command == 'rapid':
			await rapid(message, command, parameters, embed)
		elif command in ('bal', 'sup'):
			await etherscan(message, command, parameters, embed)
		elif command == 'solfloor':
			await solfloor(message, command, parameters, embed)
		elif command == 'links':
			await links(message, command, parameters, embed)
		elif command in ('rank', 'rankalert'):
			await rank(message, command, parameters, embed, notification=False, listing_price=None)
		elif command == 'floorlist':
			await floorlist(message, command, parameters, embed)
		elif command == 'sunspotrank':
			await sunspotrank(message, command, parameters, embed)
		elif command == 'whale'	and message.author.id == shalev_id:
			await whale(message, command, parameters, embed)
		elif command == 'adafloor':
			await adafloor(message, command, parameters, embed)
		elif command == 'graph':
			await graph(message, command, parameters, embed)
		elif command == 'solroyalty':
			await solroyalty(message, command, parameters, embed)
		elif command in ('profit', 'breakeven'):
			await profitbreakeven(message, command, parameters, embed)
		elif command == 'pfp':
			await pfp(message, command, parameters, embed)
		elif command == 'abi':
			await abi(message, command, parameters, embed)
		elif command == 'call':
			await call(message, command, parameters, embed)
		# elif command in 'whois':
		# 	await whois(message, command, parameters, embed)
		else:
			await message.reply("Unknown command, please refer to !help.")
		return

	if message.channel.id == channel_links_id:
		if len(message.content) < 7: return
		if any("\u0590" <= c <= "\u05EA" for c in message.content): return
		await message.reply("@everyone discord.gg/%s" % list(filter(None, message.content.replace(" ", "").split("/")))[-1])
		return

	if message.channel.id == channel_joiner_id:
		await message.reply("Fix me... 😔")
		return
		# secrets
		shalevMain = os.environ.get('shalevMain')
		shalevBurner1 = os.environ.get('shalevBurner1')
		naorMain = os.environ.get('naorMain')
		naorBurner1 = os.environ.get('naorBurner1')
		
		# join a server from a token
		def join(token, inviteCode):
			header = {"authorization": token}
			requests.post("https://discord.com/api/v8/invites/{}".format(inviteCode), headers=header)
	
		removeSpaces = message.content.replace(" ", "")
		inviteCode = removeSpaces.split("/")[-1]
		await message.reply("Trying to invite %s's tokens into discord.gg/%s" % (message.author.mention, inviteCode))
		if message.author.id == shalev_id:
			join(shalevMain, inviteCode)
			join(shalevBurner1, inviteCode)
		if message.author.id == naor_id:
			join(naorMain, inviteCode)
			join(naorBurner1, inviteCode)
		return
	if message.channel.id == channel_sunspot_id:
		if not db['sunspot_rank_enable']: return
		if message.author.id != 909830001363394593: return
		nft_id = message.embeds[0].url.split('/')[-1]
		collection = message.embeds[0].author.url.split('/')[-1]
		listing_price = message.embeds[0].fields[1].value.split()[0]

		embed = discord.Embed(color=0xE78E5A)
		command = None
		parameters = (collection, nft_id)

		await rank(message, command, parameters, embed, notification=True, listing_price=listing_price)
		return

async def help(message, command, parameters, embed):
	commands = {
		"ping": "!ping",
		"gas": "!gas eth limit gwei mints[optional]",
		"eth": "!eth amount[optional]",
		"price": "!price coin amount[optional]",
		"floor": "!floor collection[exactly as written in opensea]",
		"solfloor": "!solfloor collection[exactly as written in magiceden]",
		"royalty": "!royalty collection[exactly as written in opensea]",
		"solroyalty": "!solroyalty collection[exactly as written in magiceden]",
		"rapid": "!rapid",
		"bal": "!bal address token[optional]",
		"sup": "!sup collection/contract",
		"links": "!links collection",
		"rank": "!rank collection id",
		"rankalert": "!rankalert OR !rankalert threshold OR !rankalert me/everyone/who",
		"floorlist": "!floorlist OR !floorlist list/delete OR !floorlist collection collection collection...",
		"sunspotrank": "!sunspotrank enable/disable",
		"adafloor": "!adafloor collection[exactly as written in I DON'T FUCKING KNOW JUST TRY AGAIN]",
		"graph": "!graph collection hours[optional, default is 4]",
		"profit": "!profit collection entry_price exit_price[optional, none uses floor]",
		"breakeven": "!breakeven collection entry_price[optional, none uses floor]",
		"pfp": "!pfp user[optional, none uses self]",
		"abi": "!abi contract_address",
		"call": "!call contract_address function parameters[optional]",
	}
	if len(parameters) == 0:
		command_list = list(commands.keys())
		counter = 0
		text = ""

		def get_all(text, counter, list):
			if counter < len(list):
				text = f"{text}\n!" + list[counter]
				counter += 1
				return get_all(text, counter, list)
			else:
				return f"```{text.lstrip()}```"

		reply1 = "Argazim Tools on top 📈\nIndexed commands:\n"
		reply2 = "\nUse `!help command` to view command syntax."
		await message.reply(reply1 + get_all(text, counter, command_list) + reply2)
		return
				
	try:
		await message.reply(f"`{commands[parameters[0]]}`")
		return
	except:
		await message.reply("Command not indexed in help, please refer to !help for all the commands.")
		return

async def gas(message, command, parameters, embed):
	try:
		eth = float(parameters[0])
		limit = float(parameters[1])
		gwei = float(parameters[2])
		amount = int(parameters[3]) if len(parameters) == 4 else 1
	except:
		await message.reply("Invalid syntax, please use `!gas eth limit gwei mints[optional]`")
		return
	result = round(eth*amount+limit*gwei/1000000000, 3)
	embed.add_field(name="Cost", value=parameters[0], inline=True)
	embed.add_field(name="Gas Limit", value=parameters[1], inline=True)
	embed.add_field(name="Gwei", value=parameters[2], inline=True)
	if len(parameters) == 4 and amount != 1:
		embed.add_field(name="Quantity", value=parameters[3], inline=True)
	embed.add_field(name="Total Cost", value="**%.3f** ETH" % result, inline=False)
	await message.reply(embed=embed)

async def binance(message, command, parameters, embed):
	api = "https://api.binance.com/api/v3/ticker/price"
	coin = "ETH" if command == "eth" else parameters[0].upper()
	try:
		amount = float(parameters[1])
	except:
		try:
			amount = float(parameters[0])
		except:
			amount = 1
	params = {"symbol": f"{coin}USDC"}
	try:
		price = float(requests.get(api, params=params).json()["price"])
	except:
		await message.reply("Invalid coin/token according to the Binance API")
		return
	result = price*amount
	embed.add_field(name=f"Current Price for {amount} {coin}", value="$%.2f" % result)
	await message.reply(embed=embed)

async def nft_metrics(message, command, parameters, embed):
	collection = parameters[0]
	url = f"https://api.opensea.io/api/v1/collection/{collection}?format=json"
	r = requests.get(url)
	if r.status_code != 200:
		await message.reply("Invalid collection name, please enter exactly as written in OpenSea")
		return
	collection_json = r.json()["collection"]
	collection_name = collection_json["name"]
	collection_url = f"https://opensea.io/collection/{collection}"
	collection_image = collection_json["image_url"]
	collection_floor = collection_json["stats"]["floor_price"]
	collection_volume_24h = collection_json["stats"]["one_day_volume"]
	collection_sales_24h = collection_json["stats"]["one_day_sales"]
	collection_royalty = float(collection_json["dev_seller_fee_basis_points"])/100
	collection_royalty_str = str(collection_royalty)
	collection_royalty += 2.5
	if command == "floor":
		embed = discord.Embed(title=collection_name, url=collection_url, color=0xE78E5A)
		embed.set_footer(text="Argazim Tools", icon_url="https://i.imgur.com/8YqUQNL.png")
		embed.set_thumbnail(url=collection_image)
		embed.add_field(name="Floor Price", value=f"**{collection_floor} Ξ**", inline=True)
		embed.add_field(name="Volume 24h", value="%.2f Ξ" % collection_volume_24h, inline=True)
		embed.add_field(name="Sales 24h", value="%.0f" % collection_sales_24h, inline=True)
	elif command == "royalty":
		embed = discord.Embed(title=collection_name, url=collection_url, color=0xE78E5A)
		embed.set_footer(text="Argazim Tools", icon_url="https://i.imgur.com/8YqUQNL.png")
		embed.set_thumbnail(url=collection_image)
		embed.add_field(name=f"Royalties for {collection_name}", value=f"{collection_royalty_str}% + 2.5% = **{collection_royalty}% Total**")
	await message.reply(embed=embed)

async def rapid(message, command, parameters, embed):
	gwei_prices = requests.get(url="https://api.blocknative.com/gasprices/blockprices", headers={"Authorization": blocknative_api}).json()["blockPrices"]
	gwei_1559 = gwei_prices[0]["estimatedPrices"][0]["maxFeePerGas"]
	gwei_legacy = gwei_prices[0]["estimatedPrices"][0]["price"]
	embed = discord.Embed(title="Blocknative Gas Estimator", url="https://blocknative.com/gas-estimator", color=0xE78E5A)
	embed.set_footer(text="Argazim Tools", icon_url="https://i.imgur.com/8YqUQNL.png")
	embed.add_field(name="Legacy", value=f"**{int(gwei_legacy)}** Gwei", inline=True)
	embed.add_field(name="EIP-1559", value=f"**{int(gwei_1559)}** Gwei", inline=True)
	await message.reply(embed=embed)

async def etherscan(message, command, parameters, embed):
	def ethplorer_call(*args):
		url = "https://api.ethplorer.io/"
		params = {'apiKey': ethplorer_api}
		return requests.get(url+args[0]+'/'+address, params=params).json()

	def etherscan_call(*args):
		url = "https://api.etherscan.io/api"
		params = {
			'module': args[0],
			'action': args[1],
			'apikey': {etherscan_api},
		}
		return requests.get(url, params={**params, **args[2]}).json()

	if command == "bal":
		if len(parameters) == 0:
			await message.reply("Invalid syntax, please use `!bal address token[optional]`")
			return
		address = parameters[0] #ens.address(parameters[0]) if ".eth" in parameters[0] else parameters[0]
		address_cut = "%s...%s" % (address[0:5], address[-4::])
		ethplorer_json = ethplorer_call('getAddressInfo', address)

		if len(parameters) == 2:
			if 'tokens' in ethplorer_json.keys():
				tokens = ethplorer_json['tokens']
				token_symbol = parameters[1].upper()
			else:
				await message.reply(f"Address doesn't seem to own token `{parameters[1].upper()}`")
				return

			def get_bal(token_symbol):
				for x in range(len(tokens)): 
					if tokens[x]['tokenInfo']['symbol'] == token_symbol:
						return round(tokens[x]['balance']/10**int(tokens[x]['tokenInfo']['decimals']), 3)
					else:
						x += 1
			balance = get_bal(token_symbol)
			if balance != None and balance != 0:
				pass
			else:
				await message.reply(f"Address doesn't seem to own token `{parameters[1].upper()}`")
				return
		elif len(parameters) == 1:
			token_symbol = 'ETH'
			balance = round(ethplorer_json['ETH']['balance'], 3)
		else:
			await message.reply("Invalid syntax, please use `!bal address token[optional]`")
			return
		embed = discord.Embed(title=f"{address_cut}", url=f"https://etherscan.io/address/{address}", color=0xE78E5A)
		embed.set_footer(text="Argazim Tools", icon_url="https://i.imgur.com/8YqUQNL.png")
		embed.add_field(name=f"{token_symbol} Balance", value=f"{balance} {token_symbol}")
		await message.reply(embed=embed)
	
	elif command == "sup":
		if len(parameters) == 0:
			await message.reply("Invalid syntax, please use `!sup collection/contract`")
			return
		if len(parameters[0]) == 42:
			address = parameters[0]
			ethplorer_json = ethplorer_call('getTokenInfo', address)
			if 'totalSupply' not in ethplorer_json:
				await message.reply("Address is not a token contract")
			totalSupply = ethplorer_json['totalSupply']
			title = "%s...%s" % (address[0:5], address[-4::])
		else:
			collection = parameters[0]
			url = f"https://api.opensea.io/api/v1/collection/{collection}?format=json"
			r = requests.get(url)
			if r.status_code != 200:
				await message.reply("Invalid collection name, please enter exactly as written in OpenSea")
				return
			totalSupply = r.json()['collection']['stats']['total_supply']
			address = r.json()['collection']['primary_asset_contracts'][0]['address']
			title = "%s...%s" % (address[0:5], address[-4::])
		total_minted = int(totalSupply)
		embed = discord.Embed(title=f"{title}", url=f"https://etherscan.io/token/{address}", color=0xE78E5A)
		embed.set_footer(text="Argazim Tools", icon_url="https://i.imgur.com/8YqUQNL.png")
		embed.add_field(name=f"Total minted", value=f"{total_minted}")
		await message.reply(embed=embed)
	
	else:
		pass

async def solfloor(message, command, parameters, embed):
	collection = parameters[0]
	magiceden_api = f"http://api-mainnet.magiceden.dev/v2/collections/{collection}"
	collection_json = requests.get(magiceden_api).json()
	if 'floorPrice' not in collection_json:
		await message.reply("Invalid collection name, please enter exactly as written in MagicEden")
		return
	collection_name = collection_json['name']
	floor_price = collection_json['floorPrice']/10**9
	collection_url = f"https://magiceden.io/marketplace/{collection}"
	collection_image = collection_json['image']
	embed = discord.Embed(title=collection_name, url=collection_url, color=0xE78E5A)
	embed.set_footer(text="Argazim Tools", icon_url="https://i.imgur.com/8YqUQNL.png")
	embed.set_thumbnail(url=collection_image)
	embed.add_field(name="Floor Price", value=f"{floor_price} ◎", inline=True)
	await message.reply(embed=embed)

async def links(message, command, parameters, embed):
	collection = parameters[0]
	url = f"https://api.opensea.io/api/v1/collection/{collection}?format=json"
	r = requests.get(url).json()['collection']
	address = r['primary_asset_contracts'][0]['address']
	collection_name = r["name"]

	urls = {
		'Etherscan': "https://etherscan.io/address/%s" % address,
		'OpenSea': "https://opensea.io/collection/%s" % collection,
		'LooksRare': "https://looksrare.org/collections/%s" % address,
		'Rarible': "https://rarible.com/collection/%s" % address,
		'IcyTools': "https://icy.tools/collections/%s" % address,
		'Compass': "https://compass.art/collections/%s" % address,
		'Coniun': "https://coniun.io/collection/%s" % collection,
		'Gem': "https://www.gem.xyz/collection/%s" % address,
		'nftsniper.ai': "https://nftsniper.ai/#/collection/%s" % address,
		'TraitSniper': "https://app.traitsniper.com/%s" % collection,
		'RaritySniffer': "https://raritysniffer.com/viewcollection/%s" % collection,
		'RaritySniper': "https://raritysniper.com/%s" % address,
		'ERCRarity': "https://www.ercrarity.com/%s" % address,
	}
	text = ''
	for i, site in enumerate(urls):
		text = f"{text}[{site}]({urls[site]})\n"
	embed.add_field(name=collection_name, value=text)
	await message.reply(embed=embed)

async def rank(message, command, parameters, embed, notification, listing_price):
	if command == 'rankalert':
		if len(parameters) == 1:
			if parameters[0] in ('me', 'everyone', 'who'):
				if parameters[0] != 'who':
					db['noti_user'] = 'everyone' if parameters[0] == 'everyone' else message.author.id
				await message.reply("Rank alert notification is currently set to " + (f"<@{db['noti_user']}>" if db['noti_user'] != 'everyone' else 'everyone'))
				return
			else:
				try:
					test_int = int(parameters[0])
				except ValueError:
					await message.reply("Invalid syntax, please use !help rankalert")
					return
				db['rankalert'] = parameters[0]
		await message.reply("Rank alert is currently " + (f"set to <= {db['rankalert']}" if int(db['rankalert']) > 0 else "disabled"))
		return

	if len(parameters) != 2:
		await message.reply("Invalid syntax, please use `!rank collection id`")
		return

	collection = parameters[0]
	nft_id = parameters[1]
	opensea_url = f"https://api.opensea.io/api/v1/collection/{collection}?format=json"
	address = requests.get(opensea_url).json()['collection']['primary_asset_contracts'][0]['address']
	nftsniper_url = f"https://nftsniper.ai/#/collection/{address}"

	chrome_options = Options()
	chrome_options.add_argument('--no-sandbox')
	chrome_options.add_argument('--disable-dev-shm-usage')
	chrome_options.add_argument("--window-size=1024,576")
	driver = webdriver.Chrome(options=chrome_options)

	driver.get(nftsniper_url)
	xpath_lookup_id = "/html/body/div/div/div[2]/div/div/div[1]/div/div/form/label/div/div/div/input"
	xpath_rank = "/html/body/div[2]/div/div[2]/div/div[2]/div[1]/div[2]/div"
	xpath_image = "/html/body/div[2]/div/div[2]/div/div[1]/div[2]/img"
	xpath_name = "/html/body/div[2]/div/div[2]/div/div[2]"

	try:
		lookup_id = WebDriverWait(driver, 10).until(
			EC.presence_of_element_located((By.XPATH, xpath_lookup_id)))
		lookup_id.send_keys(nft_id)
		lookup_id.send_keys(Keys.RETURN)

		rank = WebDriverWait(driver, 10).until(
			EC.presence_of_element_located((By.XPATH, xpath_rank)))
		rarity_rank = rank.text.split('#')[-1]

		image = WebDriverWait(driver, 10).until(
			EC.presence_of_element_located((By.XPATH, xpath_image)))
		image_url = image.get_attribute("src")

		name = WebDriverWait(driver, 10).until(
			EC.presence_of_element_located((By.XPATH, xpath_name)))
		nft_name = name.text.splitlines()[2]
	except:
		driver.quit()
		return
	finally:
		driver.quit()

	listing_url = f"https://opensea.io/assets/{address}/{nft_id}"
	
	noti = False if notification is not True else True

	embed = discord.Embed(title=f"{nft_name}\nRarity Rank: {rarity_rank}", url=listing_url, color=0xE78E5A)
	embed.set_footer(text="Argazim Tools", icon_url="https://i.imgur.com/8YqUQNL.png")
	embed.set_thumbnail(url=image_url)
	await message.reply(embed=embed)
	if noti and (int(float(rarity_rank)) <= int(float(db['rankalert']))):
		await message.reply((f"<@{db['noti_user']}>" if db['noti_user'] != 'everyone' else "@everyone") + f" {nft_name} RANK {rarity_rank} FOR {listing_price}")

async def floorlist(message, command, parameters, embed):
	if len(parameters) == 0:
		try:
			test_value = db[f'floorlist.{message.author.id}']
		except KeyError:
			await message.reply(f"Project list not set for <@{message.author.id}>")
			return

		for project in db[f'floorlist.{message.author.id}']:
			await nft_metrics(message, 'floor', [project], embed)
	elif parameters[0] == 'delete':
		try:
			test_value = db[f'floorlist.{message.author.id}']
		except KeyError:
			await message.reply(f"Project list already not set for <@{message.author.id}>!")
			return
		del db[f'floorlist.{message.author.id}']
		await message.reply(f"Deleted project list for <@{message.author.id}>!")
	else:
		if parameters[0] != 'list':
			db[f'floorlist.{message.author.id}'] = list(parameters)
		await message.reply(f"<@{message.author.id}>'s project list:")
		await message.channel.send(' '.join(db[f'floorlist.{message.author.id}']))

async def sunspotrank(message, command, parameters, embed):
	if len(parameters) != 1:
		await message.reply("Invalid syntax, please use `!sunspotrank enable/disable`")
		return		
	if parameters[0] == 'enable':
		db['sunspot_rank_enable'] = True
	elif parameters[0] == 'disable':
		db['sunspot_rank_enable'] = False
	else:
		await message.reply("Invalid syntax, please use `!sunspotrank enable/disable`")
		return
	await message.reply(f"Sunspot rank monitor {('enabled' if db['sunspot_rank_enable'] else 'disabled')}")

async def whale(message, command, parameters, embed):
	if len(parameters) != 1:		
		await message.reply("Invalid syntax, please use `!whale enable/disable`")
		return	
	if parameters[0] == 'enable':
		db['whale'] = True
	elif parameters[0] == 'disable':
		db['whale'] = False
	else:
		await message.reply("Invalid syntax, please use `!whale enable/disable`")
		return
	await message.reply(f"Whale alert {('enabled' if db['whale'] else 'disabled')}")

async def adafloor(message, command, parameters, embed):
	collection = ' '.join(parameters)
	policy_api = f"https://raw.githubusercontent.com/Cardano-NFTs/policyIDs/main/projects/{collection}"
	r1 = requests.get(policy_api)
	if r1.status_code != 200:
		await message.reply("Invalid collection name")
		return
	r1_json = r1.json()
	if 'project' not in r1_json:
		r1_json = r1_json[0]
	policy_id = r1_json['policies'][0]
	opencnft_api = f"https://api.opencnft.io/1/policy/{policy_id}"
	r2 = requests.get(opencnft_api)
	opencnft_json = r2.json()
	floor_price = opencnft_json['floor_price']/10**6
	collection_image = "https://ipfs.io/ipfs/%s" % opencnft_json['thumbnail'].split('/')[-1]

	embed = discord.Embed(title=collection, color=0xE78E5A)
	embed.set_footer(text="Argazim Tools", icon_url="https://i.imgur.com/8YqUQNL.png")
	embed.set_thumbnail(url=collection_image)
	embed.add_field(name="Floor Price", value="%.0f ₳" % floor_price, inline=True)
	await message.reply(embed=embed)

async def graph(message, command, parameters, embed):
	collection = parameters[0]
	url = f"https://api.opensea.io/api/v1/collection/{collection}?format=json"
	os_r = requests.get(url)
	if os_r.status_code != 200:
		await message.reply("Invalid collection name, please enter exactly as written in OpenSea")
		return
	collection_json = os_r.json()["collection"]
	collection_name = collection_json["name"]
	collection_url = f"https://opensea.io/collection/{collection}"

	date = datetime.datetime.now()
	unix_time_now = datetime.datetime.timestamp(date)

	unix_time_start = unix_time_now - (14400 if len(parameters) == 1 else int(parameters[1])*3600)
	sunspot_api = "https://dpldouen3w8e7.cloudfront.net/production/events-scatterplot"
	params = {
		'collectionSlug': collection,
		'startCreatedAtMinuteTime': unix_time_start,
		'endCreatedAtMinuteTime': unix_time_now,
	}
	sunspot_r = requests.get(url=sunspot_api, params=params)

	embed = discord.Embed(title=collection_name, url=collection_url, color=0xE78E5A)
	embed.set_footer(text="Argazim Tools", icon_url="https://i.imgur.com/8YqUQNL.png")
	embed.set_image(url=sunspot_r.url)
	await message.reply(embed=embed)

async def solroyalty(message, command, parameters, embed):
	collection = parameters[0]
	magiceden_api = f"https://api-mainnet.magiceden.dev/v2/collections/{collection}"

	collection_json = requests.get(magiceden_api).json()
	if 'symbol' not in collection_json:
		await message.reply("Invalid collection name, please enter exactly as written in MagicEden")
		return

	token_api = f"https://api-mainnet.magiceden.dev/v2/tokens/{requests.get(magiceden_api+'/activities?offset=0&limit=1').json()[0]['tokenMint']}"
	royalty = requests.get(token_api).json()['sellerFeeBasisPoints']/100
	
	collection_name = collection_json['name']
	collection_url = f"https://magiceden.io/marketplace/{collection}"
	collection_image = collection_json['image']
	embed = discord.Embed(title=collection_name, url=collection_url, color=0xE78E5A)
	embed.set_footer(text="Argazim Tools", icon_url="https://i.imgur.com/8YqUQNL.png")
	embed.set_thumbnail(url=collection_image)
	embed.add_field(name=f"Royalties for {collection_name}", value=f"{royalty}% + 2% = **{float(royalty) + 2}% Total**", inline=True)
	await message.reply(embed=embed)

async def profitbreakeven(message, command, parameters, embed):
	if len(parameters) not in (1, 2, 3):
		if command == 'profit':
			await message.reply("Invalid syntax, please use `!profit collection entry_price exit_price[optional, none uses floor]`")
			return
		elif command == 'breakeven':
			await message.reply("Invalid syntax, please use `!breakeven collection entry_price[optional, none uses floor]`")
			return

	collection = parameters[0]

	url = f"https://api.opensea.io/api/v1/collection/{collection}?format=json"
	r = requests.get(url)
	if r.status_code != 200:
		await message.reply("Invalid collection name, please enter exactly as written in OpenSea")
		return
	collection_json = r.json()["collection"]
	collection_name = collection_json["name"]
	collection_url = f"https://opensea.io/collection/{collection}"
	collection_image = collection_json["image_url"]
	collection_floor = float(collection_json["stats"]["floor_price"])
	collection_royalty = float(collection_json["dev_seller_fee_basis_points"])/100
	collection_royalty_final = collection_royalty + 2.5

	embed = discord.Embed(title=collection_name, url=collection_url, color=0xE78E5A)
	embed.set_footer(text="Argazim Tools", icon_url="https://i.imgur.com/8YqUQNL.png")
	embed.set_thumbnail(url=collection_image)
	
	if command == 'breakeven':
		if len(parameters) == 2:
			try:
				entry = float(parameters[1])
			except:
				await message.reply("Invalid syntax, please use `!breakeven collection entry_price[optional, none uses floor]`")
				return
		elif len(parameters) == 1:
			entry = collection_floor
		breakeven_price = entry / (1 - collection_royalty_final/100)
		embed.add_field(name=f"Entry Price", value=f"{entry} Ξ", inline=True)
		embed.add_field(name=f"Breakeven Price", value="**%.3f Ξ**" % breakeven_price, inline=True)
		await message.reply(embed=embed)
		return	

	try:
		entry_price = float(parameters[1])
	except:
		await message.reply("Invalid syntax, please use `!profit collection entry_price exit_price[optional, none uses floor]`")
		return
	embed.add_field(name=f"Entry Price", value=f"{entry_price} Ξ", inline=True)

	if len(parameters) == 3:
		try:
			exit_price = float(parameters[2])
		except:
			await message.reply("Invalid syntax, please use `!profit collection entry_price exit_price[optional, none uses floor]`")
			return
		profit = exit_price * (1 - collection_royalty_final/100) - entry_price
		embed.add_field(name=f"Exit Price", value=f"{exit_price} Ξ", inline=True)
	else:
		profit = collection_floor * (1 - collection_royalty_final/100) - entry_price
		embed.add_field(name=f"Current Floor", value=f"{collection_floor} Ξ", inline=True)
	
	embed.add_field(name=f"Total Profit", value="**%s %.3f Ξ**" % ('📈' if profit > 0 else '📉', profit))
	await message.reply(embed=embed)

async def pfp(message, command, parameters, embed):
	user_id = message.author.id if len(parameters) == 0 else message.mentions[0].id
	pfp_hash = message.author.avatar if len(parameters) == 0 else message.mentions[0].avatar
	pfp_url = f"https://cdn.discordapp.com/avatars/{user_id}/{pfp_hash}.png?size=1024"
	embed.set_image(url=pfp_url)
	await message.reply(embed=embed)

async def abi(message, command, parameters, embed):
	contract_address = parameters[0]

	def etherscan_call(*args):
			url = "https://api.etherscan.io/api"
			params = {
				'module': args[0],
				'action': args[1],
				'apikey': {etherscan_api},
			}
			return requests.get(url, params={**params, **args[2]}).json()

	r = etherscan_call('contract', 'getabi', {'address': contract_address})
	if r['status'] == '0':
		await message.reply('Address is not a contract or contract is unverified.')
		return
	contract_abi = r['result']
	with open('abi.txt', 'w') as file:
		file.write(contract_abi)
	await message.reply(file=discord.File('abi.txt'))
	os.remove('abi.txt')

async def call(message, command, parameters, embed):
	try:
		contract_address = parameters[0]
		contract_function = parameters[1]
		contract_arguments = parameters[2:]
	except IndexError:
		await message.reply("Syntax error, please refer to `!help call`")
		return

	def etherscan_call(*args):
			url = "https://api.etherscan.io/api"
			params = {
				'module': args[0],
				'action': args[1],
				'apikey': {etherscan_api},
			}
			return requests.get(url, params={**params, **args[2]}).json()
	contract_abi = etherscan_call('contract', 'getabi', {'address': contract_address})['result']

	web3_contract = w3.eth.contract(address=contract_address, abi=contract_abi)
	arguments = []
	for argument in contract_arguments:
		if argument.isdigit():
			arguments.append(int(argument))
		else:
			arguments.append(argument)
	try:
		contract_call = getattr(web3_contract.functions, contract_function)(*arguments).call()
		await message.reply(contract_call)
	except Exception as error:
		await message.reply(error)

# async def derisk(message, command, parameters, embed):
# 	tx_hash = parameters[0]

# 	def ethplorer_call(*args):
# 		url = "https://api.ethplorer.io/"
# 		params = {'apiKey': ethplorer_api}
# 		return requests.get(url+args[0]+'/'+tx_hash, params=params)

# 	r = ethplorer_call('getTxInfo', tx_hash)
# 	if r.status_code != 200:
# 		await message.reply("Invalid tx hash")
# 	ethplorer_json = r.json()

# 	embed = discord.Embed(title=collection_name, url=collection_url, color=0xE78E5A)
# 	embed.set_footer(text="Argazim Tools", icon_url="https://i.imgur.com/8YqUQNL.png")
# 	embed.set_thumbnail(url=collection_image)
# 	embed.add_field(name=f"Tx Value", value=f"{tx_value} Ξ", inline=True)
# 	embed.add_field(name=f"Tx Fee", value=f"{tx_fee} Ξ", inline=True)
# 	embed.add_field(name=f"Royalties", value=f"{royalties_final}%", inline=True)
# 	embed.add_field(name=f"Breakeven", value=f"{breakeven_price} Ξ", inline=True)

# async def whois(message, command, parameters, embed):
# 	user_id = parameters[0]
# 	url = f"https://discord.com/api/users/{user_id}"
# 	headers = {"authorization": f"Bot {token}"}
# 	user_json = requests.get(url, headers=headers).json()
# 	username = user_json['username'] + '#' + user_json['discriminator']
# 	avatar_id = user_json['avatar']
# 	pfp_url = f"https://cdn.discordapp.com/avatars/{user_id}/{avatar_id}.png?size=1024"

# 	embed = discord.Embed(title=f"{username}", color=0xE78E5A)
# 	embed.set_footer(text="Argazim Tools", icon_url="https://i.imgur.com/8YqUQNL.png")
# 	embed.set_thumbnail(url=pfp_url)
# 	await message.reply(embed=embed)

keep_alive()
client.run(token)