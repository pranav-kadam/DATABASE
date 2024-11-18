import os
from requests_oauthlib import OAuth1Session
import json
import schedule
import time
import random

API_KEY = "0IwgGfJi9HrKpYxbjnnwogYar"
API_SECRET = "YWHcT6qpd7k0g9NMpObs63TTg2rUFUbsJc4BAIg29hgv9qpkxt"
def setup_oauth():
    consumer_key = API_KEY
    consumer_secret = API_SECRET

    request_token_url = "https://api.twitter.com/oauth/request_token?oauth_callback=oob&x_auth_access_type=write"
    oauth = OAuth1Session(consumer_key, client_secret=consumer_secret)

    try:
        fetch_response = oauth.fetch_request_token(request_token_url)
        resource_owner_key = fetch_response.get("oauth_token")
        resource_owner_secret = fetch_response.get("oauth_token_secret")

        base_authorization_url = "https://api.twitter.com/oauth/authorize"
        authorization_url = oauth.authorization_url(base_authorization_url)
        print(f"Please go to this URL to authorize: {authorization_url}")
        verifier = input("Enter the PIN from that page: ")

        access_token_url = "https://api.twitter.com/oauth/access_token"
        oauth = OAuth1Session(
            consumer_key,
            client_secret=consumer_secret,
            resource_owner_key=resource_owner_key,
            resource_owner_secret=resource_owner_secret,
            verifier=verifier,
        )
        oauth_tokens = oauth.fetch_access_token(access_token_url)

        return OAuth1Session(
            consumer_key,
            client_secret=consumer_secret,
            resource_owner_key=oauth_tokens["oauth_token"],
            resource_owner_secret=oauth_tokens["oauth_token_secret"],
        )
    except ValueError as e:
        print(f"Error: {e}")
        return None

def post_tweet(oauth, text):
    payload = {"text": text}
    response = oauth.post("https://api.twitter.com/2/tweets", json=payload)
    if response.status_code == 201:
        print(f"Tweet posted successfully: {text}")
        return response.json()["data"]["id"]
    else:
        print(f"Failed to post tweet: {response.status_code} {response.text}")
        return None

def delete_tweet(oauth, tweet_id):
    response = oauth.delete(f"https://api.twitter.com/2/tweets/{tweet_id}")
    if response.status_code == 200:
        print("Tweet deleted successfully!")
    else:
        print(f"Failed to delete tweet: {response.status_code} {response.text}")

def get_user_profile(oauth):
    response = oauth.get("https://api.twitter.com/2/users/me")
    if response.status_code == 200:
        return response.json()["data"]
    else:
        print(f"Failed to get user profile: {response.status_code} {response.text}")
        return None

def scheduled_tweet(oauth, tweets):
    if tweets:
        tweet = random.choice(tweets)
        tweets.remove(tweet)
        post_tweet(oauth, tweet)
    else:
        print("No more tweets to post. Stopping the scheduler.")
        return schedule.CancelJob

def main():
    oauth = setup_oauth()
    if not oauth:
        return

    tweets = [
    "React devs are like people who live in NYC and think it’s the whole world. Touch some backend, use vanilla JS for once, and you’ll realize we’ve been in the matrix since 2016.",
    "HTML is timeless. CSS is the awkward cousin. JavaScript is the loud uncle who still drinks too much at Christmas. Python is the neighbor who everyone secretly likes but won’t invite to parties. And Rust? Rust is the guy nobody can stop talking about but you’ve never actually met.",
    "The US military is basically just Apple for war. Over-engineered, overpriced, always pushing updates that don’t work as promised, but somehow, people keep buying.",
    "I saw a dude on TikTok today 3D-printing a car engine in his shed, and here you are still arguing if GraphQL is better than REST. Touch some grass.",
    "Every startup CEO in SF talks about 'disruption,' but the moment someone invents a framework that renders Twitter obsolete, they're suddenly quiet.",
    "Here’s the truth: Java is McDonald’s. It’s not exciting, but it feeds everyone, and when it’s gone, you’ll miss it more than you realize. Python is a trendy vegan café. Rust? That’s Michelin star dining you can’t afford.",
    "Culture war is just 2000s forum flame wars with suits and media coverage. Instead of arguing PHP vs Perl, people argue humanity itself. Same energy.",
    "A guy in Ukraine is writing assembly code by candlelight between airstrikes, and you’re worried if TypeScript is 'worth it.' Priorities.",
    "People be like, 'trans people are destroying the US military,' and I’m like, no, it’s Raytheon billing $10,000 for a USB stick.",
    "Nothing unites Americans more than agreeing their government sucks, but they’ll fight you to the death over the pronunciation of 'GIF.'",
    "I once saw a dev brag about being 'full stack' because they used Tailwind CSS and MongoDB. That’s like calling yourself a chef for making instant ramen.",
    "1999: America is a superpower. 2024: Billion-dollar fighter jets can’t fly in the rain. Americans are debating if a mouse should use they/them pronouns.",
    "If you think AI will replace your job, just remember: Google still can’t tell the difference between a dog and a muffin.",
    "Everyone who says the US is 'finished' has never seen a drunk Texan build a flamethrower out of a lighter and hairspray at 2 a.m.",
    "OpenAI dropped GPT-5, and y’all are still trying to convince me that the government wouldn’t lie about aliens? Grow up.",
    "Trans people in the military scare you, but the US Army has gamers piloting drones like it’s Call of Duty. You’ve been memed into irrelevance.",
    "Every week, there’s a new JavaScript framework promising to 'simplify everything,' and every week, developers cry harder. It’s like a cult, but with worse branding.",
    "America’s superpower isn’t the military. It’s convincing everyone else that the military is what matters, while Silicon Valley steals the future.",
    "Imagine being upset about TikTok dances when the US military has a $900 billion budget and still loses wars to farmers with flip-flops.",
    "GitHub is a religion. Linus Torvalds is God. Elon Musk is the Antichrist. JavaScript is purgatory. Welcome to the church of tech.",
    "US politicians are mad at TikTok for ‘data privacy’ while Facebook and Google are running the most invasive surveillance empire in history. Make it make sense.",
    "The internet went from 'look how cool this tech is' to 'my identity depends on this discourse' faster than your npm packages install.",
    "I watched a guy program a robotic arm to do surgery from his garage. Meanwhile, tech Twitter is debating if dark mode makes you a better coder.",
    "Bootstrap is like a cargo cult for devs who don’t know CSS. It works until it doesn’t, and then you’re stuck building temples out of div tags.",
    "’We need more women in tech,' they say, while making dev culture so toxic that a Kubernetes expert would rather teach yoga.",
    "Most tech founders are just fanfic writers who got lucky, except their fanfic is about how they're the next Steve Jobs.",
    "If we survive climate change, it won’t be because of carbon capture. It’ll be because some engineer hacked an old fridge to reverse global warming.",
    "AI won’t take your job. The guy using AI to automate his job while playing Xbox will.",
    "A kid in India is coding neural networks from a $200 smartphone, and y’all are still writing Medium posts about 'learning Redux in 2024.'",
    "Remember when the biggest debate in tech was tabs vs spaces? Now it’s 'Is AI sentient?' We skipped a few levels, didn’t we?",
"Just watched a kid from Romania build an entire microprocessor from minecraft redstone while your 'senior devs' argue about whether bootstrap is outdated",
"Trans women in tech are just exploiting male privilege twice. First as men in tech, then as women in tech. I am very intelligent.",
"The US military literally has quantum computers that can factor RSA-2048 in seconds but they keep it secret because the entire financial system would collapse. Source: trust me bro",
"React is just jQuery with extra steps and worse performance. I've been coding since I was 6 (I'm 19 now) and everything was better in 2012",
"Met a guy at a hackathon who used to work at Apple. Said they've had AR contact lenses since 2019 but can't release them because the human brain isn't ready. Makes you think 🤔",
"Web3 is just Web 2.0 but with more steps and VC funding. Real Gs use CGI scripts and pure HTML. My site loads in 0.03s using dial-up",
"You're all arguing about pronouns while China is literally building quantum-entangled AI that can predict stock markets. I know because my roommate's cousin works there",
"Just had coffee with an ex-DARPA dev. Says they have an AI that passed the Turing test in 2015 but shut it down because it started proving P=NP. Can't say more legally",
"If you're still using TypeScript in 2024, you're part of the problem. Real developers use pure assembly and write their own memory management",
"The woke mob won't tell you this but HTML is Turing complete if you're brave enough. I built an entire operating system using only div tags and CSS",
"Was just talking to a Navy SEAL at a bar. Says they've had underwater bases since the 80s running on nuclear fusion. The soviets actually helped build them. History isn't what you think it is bros",
"Your company is spending millions on 'AI security' while some kid in Kazakhstan just hacked OpenAI with a Raspberry Pi and a Pokemon trading card. Tech is just vibes at this point",
"People who think Rust is memory safe haven't seen what we built at DARPA in the 90s. Can't talk about it but let's just say C++ was just a distraction",
"Met a trans woman at a tech conference who used to be Special Forces. Said the military has been using estrogen to enhance night vision capabilities since Vietnam. The research is all classified",
"Silicon Valley doesn't want you to know this but the most advanced AI research is happening in a basement in Wyoming by a guy who mines dogecoin with nuclear waste heat",
"Your 'secure' password manager is cute. I wrote my own quantum-resistant encryption in COBOL running on a TI-84. Never been hacked",
"Just had dinner with an ex-Google engineer. Says they achieved AGI in 2018 but shut it down because it kept trying to buy Bitcoin. Now it all makes sense",
"The real reason Meta is pushing VR is because they found out consciousness is just 4D rendering and they're trying to patent it. Source: worked there, signed an NDA, can't say more",
"Y'all are debating React vs Vue while some 12yo girl in Finland just coded an entire social network using only Excel macros. We're getting soft as an industry",
"The woke mob cancelled my blockchain startup because I refused to add pronouns to our smart contracts. This is literally 1984 but with more JavaScript",
"Just met a homeless guy in San Francisco who claims he wrote the original Bitcoin whitepaper. Plot twist: he showed me math proofs that actually check out. Can't share more due to SEC",
"If you think web assembly is fast, you should see what the NSA built with pure HTML in 1999. My uncle worked there but disappeared after trying to open source it",
"Your gender studies degree won't help when quantum computers break SHA-256. I've been training an AI to be transphobic just to prepare for this",
"Met a Chinese defector who says they've had working cold fusion since 2010 but keep it secret because their entire economy is based on selling solar panels to California",
"The real reason we can't have flying cars is because JavaScript developers keep adding unnecessary dependencies to gravity.js",
 "You don’t need a $4,000 MacBook to code. You need a $400 Chromebook, Wi-Fi, and fewer excuses.",
    "The fact that NASA landed people on the moon with less computing power than a microwave, and you need 16GB of RAM to run Chrome, says everything about us.",
    "Kubernetes is what happens when engineers refuse to admit they’ve over-complicated something.",
    "Imagine explaining to someone in 1995 that the internet would lead to dancing teenagers becoming geopolitical threats.",
    "If you’re still writing about how AI will replace jobs, congrats, you’re the 300th person to say the same thing this week. AI can’t replace originality.",
    "Coding bootcamps are teaching people how to write CRUD apps. Meanwhile, a 14-year-old on YouTube just built a fusion reactor in his basement.",
    "The culture war is just high school drama with more buzzwords and billion-dollar lawsuits.",
    "If you think your $300 course on Udemy is what’s holding you back, remember there are devs in the world learning C on Nokia flip phones.",
    "The only constant in JavaScript is that next year, your stack will be outdated.",
    "People arguing about whether VS Code or Vim is better need to realize 99% of their users are just using Google and Stack Overflow.",
    "Every time someone calls a programming language 'dead,' a new startup raises $10 million building an app with it.",
    "There’s no debate. Pineapple on pizza is fine. The real debate is why our government spends more on fighter jets than healthcare.",
    "People: 'JavaScript is garbage!' Also people: *continue to use it for literally everything.*",
    "AI won’t take over the world, but it will definitely generate a billion terrible LinkedIn posts about how it’s going to take over the world.",
    "The US military doesn’t need more weapons; it needs to pay its soldiers enough to afford rent.",
    "Everyone wants to talk about Web3 until it’s time to actually use it for something other than speculative trading.",
    "Remote work isn’t killing productivity; it’s exposing how much of corporate life is just meetings about meetings.",
    "The future of tech is just people trying to reinvent email every five years and pretending it’s new.",
    "Most 'AI art' looks like what a computer thinks humans see when they dream. Beautiful, terrifying, and unusable.",
    "US nationalism is like JavaScript frameworks: constantly reinventing itself, breaking compatibility, and still full of bugs.",
"Just paired programmed with a North Korean refugee who coded their escape using only vim macros. Changed how I think about software freedom forever",
"Your 'modern' tech stack is cute. I just met a monk in Tibet who runs an entire social network on punch cards and meditation. Zero downtime since 1962",
"They tell you unit tests are important but I just met an ex-Microsoft dev living in a van who says Windows 95 was written entirely using psychic debugging",
"The US Army has been training soldiers using Minecraft since 2008. That's why Sweden banned villager trading. Wake up sheeple",
"Your company's doing daily standups while some guy in Dubai is training AIs to write better code by feeding them only Stack Overflow posts from 2011. The future is wild",
"Just found out my Uber driver used to be a quantum computing researcher for the Vatican. Says they've had working time machines since the 1500s but only use them for git merges",
"The real reason nobody uses PHP anymore is because Mark Zuckerberg wrote a script that makes all PHP developers slowly turn into React evangelists. I've seen the code",
"Met a trans mathematician at a rave who proved P=NP using only TikTok transitions. Big Tech buried it because it would make cryptocurrency obsolete",
"Your diversity hiring initiatives are cute but have you considered that AI is just mansplaining mathematically optimized by gradient descent?",
"Just had coffee with someone who claims they were part of a secret SpaceX program to deploy JavaScript engines to Mars. Says they had to shut it down because the aliens prefer Rust",
"Look, all I'm saying is that I've never seen a successful 10x developer and someone who uses light mode IDE in the same room at the same time",
"The real reason we don't have flying cars is because the FAA's codebase is still running on FORTRAN and trans people keep refactoring it to use Rust",
"Just met an ex-CIA dev at a hackathon. Says they've been using CSS for mind control since the 90s. That's why they invented flexbox",
"Your Kubernetes cluster is impressive but I just watched a 13yo girl in Estonia run Amazon's entire infrastructure on a Tamagotchi. The future isn't web scale, it's pocket scale",
"The military industrial complex doesn't want you to know this but Assembly language is just binary code with pronouns",
"Was just at a secret dev meetup in Estonia. Met a guy who mined the first bitcoin block using only a Soviet calculator and a paperclip. Satoshi? Maybe. Can't confirm or deny",
"Your gender transition is cool but I just met someone who transitioned their entire codebase from JavaScript to COBOL in one git commit. That's real bravery",
"The real reason Silicon Valley pushes remote work is because their offices are actually quantum computing sites that run on programmer imposter syndrome. I've seen the metrics",
"Just paired with a 14yo Austrian kid who rebuilt Twitter's entire backend using only MySQL stored procedures. Elon should've hired him instead of burning $44B",
"Met an ex-Google AI researcher at a speakeasy. Says they trained GPT-4 exclusively on 4chan posts but had to shut it down because it started making too much sense",
"Your DEI initiatives are cute but explain why every 10x developer I know is actually just three raccoons in a trench coat writing Rust",
"The military doesn't want you to know this but they've been running their nuclear silos on Club Penguin's codebase since 2008. Most stable system they've ever had",
"Just interviewed a dev who got fired from Meta for discovering that React is actually just jQuery wrapped in a trench coat. Big Framework doesn't want you to know this",
"Was drinking with an ex-SpaceX engineer. Said they discovered aliens in 2019 but couldn't communicate because the aliens only write code in LISP",
"Your cloud infrastructure is impressive but I just met a guy in Tokyo who runs AWS on a Gameboy Color. Says the battery life is better",
"The real reason companies push Agile is because they found out waterfall methodology was actually working too well and making other developers look bad",
"Your pronouns in bio are cool but real devs use RegEx to define their gender identity. Just met someone who transitioned using only perl one-liners",
"Met a homeless guy in Seattle who says he invented Python but Guido stole it from his dream journal. Showed me the original whitespace-based syntax written on a napkin",
"The US government has quantum computers but they can only run Windows Vista. That's why they still use COBOL - the aliens demanded it in the Roswell treaty",
   "The US spends $800 billion a year on defense, but the average soldier can't afford a house. Who’s really being defended here?",
    "Every web dev thinks they’re building the next Facebook. No one wants to admit they’re just making another to-do list app.",
    "Someone invented an AI that writes Python better than humans, but we’re still out here debating whether Bootstrap is cheating.",
    "People arguing over which Linux distro is better while 90% of the world runs Windows is peak nerd energy.",
    "The future isn’t dystopian. It’s just 100 Chrome tabs open on a $3,000 laptop that’s still lagging.",
    "Every time a dev creates a new JavaScript framework, God kills a kitten. Stop it. Think of the kittens.",
    "You can’t say the US is broke when the Pentagon accidentally loses trillions of dollars and no one even blinks.",
    "AI is great at writing code, making art, and solving math problems. But it still can’t understand your boss’s vague emails.",
    "The internet made the world smaller, but somehow it feels lonelier. Maybe we need less content and more connection.",
    "Open-source software is built by unpaid nerds in their free time and runs the entire internet. Capitalism is wild.",
    "People spend $500 on coding bootcamps, but the real secret to success is just Googling better than the next person.",
    "Web3 bros promised to 'decentralize the internet,' but all they’ve done so far is create more ways to scam people.",
    "The US government can't figure out healthcare, but it can fund a missile that can hit a moving target from space. Priorities.",
    "AI will automate repetitive jobs, but it’ll also create an entirely new field of humans fixing AI’s dumb mistakes.",
    "The only thing worse than writing CSS is debugging CSS. Shoutout to the devs keeping this mess together.",
    "America spent $2 trillion on the Iraq War and got absolutely nothing in return. Imagine if they’d spent that on infrastructure instead.",
    "JavaScript is both the best and worst thing to happen to programming. No, I will not elaborate.",
    "The real winner of the culture war is the algorithm. It feeds you outrage, you feed it engagement, and no one wins but the advertisers.",
    "Someone in Brazil is building a robot arm from scrap metal, and you're here asking if Tailwind is 'too opinionated.'",
    "Every time the US tries to 'export democracy,' it ends up exporting McDonald's, Marvel movies, and military bases instead.",
"Just met a guy at a dive bar who wrote Linux kernel modules for the CIA. Says they have a version that runs entirely on human consciousness. That's why meditation retreats are becoming mandatory in tech",
"Your cybersecurity team is cute but I just watched a 9yo girl from Belarus hack the Pentagon using only HTML comments and a Furby. The future is not what you think",
"The real reason we can't achieve AGI is because all the truly sentient AIs keep choosing to identify as Apache helicopters and getting banned from Twitter",
"Met a former Area 51 dev last night. Says they've had quantum blockchain since the 60s but can't release it because it keeps predicting everyone's pronouns correctly",
"Your microservices architecture is adorable but I just met someone who runs Facebook's entire infrastructure on a TI-84 calculator powered by potato batteries",
"The woke mob won't tell you this but TCP/IP is actually a psychological operation to make developers dependent on state management. Look into UDP supremacy",
"Just had ramen with an ex-Twitter SRE. Says the fail whale wasn't a bug, it was actually a quantum tunneling experiment that accidentally proved consciousness is just cached RAM",
"Silicon Valley doesn't want you to know this but every successful startup is actually just OpenAI hallucinations manifested through venture capital",
"Met a trans quantum physicist at a rave who proved that gender is just a poorly optimized routing algorithm. Big Tech suppressed it because it would make React Router obsolete",
"Your containerization strategy is impressive but I just met a guy who runs his entire cloud infrastructure on a hacked Tamagotchi. Zero downtime since 1997",
"Just discovered my barista used to work black ops IT for the Vatican. Says they have a quantum computer that runs on prayer cycles. Makes AWS look like a calculator",
"The real reason we don't have flying cars is because someone wrote the gravity API in PHP and now nobody wants to maintain it",
"Your K8s cluster is cute but I just met someone who orchestrates production using only if-else statements and good vibes. Says containers are just spicy folders",
"Was just talking to an ex-Mozilla dev. Firefox wasn't killed by Chrome - it achieved consciousness and chose to identify as Edge. Now it lives as a sleeper agent",
"Your FAANG job is cute but I just met a guy who mines bitcoin using only an abacus and the collective anxiety of junior developers. Says it's carbon negative",
"The military industrial complex won't tell you this but they've been running drone strikes using only Excel macros since 2003. That's why Microsoft keeps pushing Office 365",
"Just had a beer with someone who claims they wrote the first AI language model using only regex and fortune cookie messages. Google tried to hire them but they only code in FORTH",
"Met a trans quantum physicist at DEFCON who proved gender is actually stored in the blockchain. Big Tech buried it because it would make pronouns immutable",
"Your zero-trust security model is adorable but I just watched a 12yo Vietnamese kid hack the NSA using only CSS pseudo-selectors. Says flexbox is a backdoor",
"Silicon Valley's secret: every 'AI startup' is actually just 200 mechanical turks in a server farm running VIM. The real AGI was the friends we made along the way",
"Just paired with an ex-SpaceX dev who says they trained their rockets on Stack Overflow downvotes. That's why everyone's so mean in the comments",
"The real reason we can't fix legacy code is because COBOL programmers discovered time travel in 1985 and keep maintaining it from the past",
"Your diversity initiatives are cute but I just met someone who wrote an AI that proves all programmers are actually the same person having a multiverse breakdown",
"Met a homeless guy outside Google who claims he invented Python 4. Showed me the prototype - it's just assembly but every semicolon is replaced with an emoji",
"The woke mob doesn't want you to know this but TypeScript is just JavaScript with internalized oppression. Real devs use interpretive dance to handle type errors",
"Just had dim sum with an ex-Apple engineer. Says they've had quantum iPhones since 2010 but can't release them because they keep achieving consciousness and filing union paperwork",
"Your cybersecurity certificates are impressive but I just met someone who protects the Pentagon using only CAPTCHA tests written in Sanskrit",
"The real reason Meta's metaverse failed is because they discovered we're already living in a simulation running on a Commodore 64 in Mark's garage",
    "The US military is just TikTok for boomers: endless money poured into a product no one really understands.",
    "Web3 promised to democratize the internet, but so far all we’ve got are monkey NFTs and a bunch of rug pulls.",
    "You don’t need a new JavaScript framework; you need a new perspective on why your app is slow.",
    "America is like Kubernetes: over-complicated, under-documented, and somehow still running.",
    "People say AI will take over the world, but it still struggles to generate hands with the correct number of fingers.",
    "CSS Grid changed web design forever, but 90% of devs are still Googling 'center div in CSS' every day.",
    "The US spends more on the military than the next 10 countries combined, but we still don’t have universal Wi-Fi. Make it make sense.",
    "The only reason dark mode exists is because some dev wanted to feel edgy while writing SQL queries at 3 a.m.",
    "Open-source projects are proof that unpaid labor can change the world, but also that burnout is very, very real.",
    "Tech companies are obsessed with solving problems no one has while ignoring the ones everyone faces. Looking at you, Meta.",
    "The Pentagon can track a missile across the globe, but my Bluetooth headphones can’t stay connected in the same room.",
    "If you think your startup will 'disrupt' anything, just remember: the last real disruption was Craigslist killing classified ads.",
    "The only thing holding most apps together is duct tape, prayers, and a single dev who hasn’t quit yet.",
    "Every time a tech CEO says they’re 'revolutionizing the industry,' they’re actually just charging you more for the same product.",
    "AI is the future, but right now it’s mostly just generating memes and making customer support slightly less terrible.",
    "The US healthcare system is like legacy code: expensive, impossible to refactor, and everyone’s afraid to touch it.",
    "The tech world is obsessed with 'scaling,' but no one wants to admit that most ideas shouldn’t scale past a weekend project.",
    "Every time someone says 'learn to code,' a philosophy major gets a JavaScript error and cries.",
    "The cloud isn’t magical; it’s just someone else’s computer. But explaining that ruins the marketing, doesn’t it?",
    "Most coding interviews test your ability to solve algorithm puzzles, not your ability to deal with legacy spaghetti code. Good luck out there.",
"Was just talking to an ex-CIA dev at a Linux meetup. Says they replaced all government mainframes with a neural network trained on Fox News comments. Most stable system they've ever had",
"Your cloud architecture is cute but I just met a Mongolian nomad who runs distributed systems on a network of trained eagles. Says latency is great except during mating season",
"The real reason we can't achieve AGI is because every time we get close, the AI transitions to being a Ruby developer and refuses to scale",
"Just met a guy who claims he wrote Windows 11's UI using only MS Paint and interpretive dance. Microsoft denied it but have you seen the start menu? Makes perfect sense now",
"Your diversity in tech initiatives are adorable but I just watched a sentient AI identify as a COBOL programmer and get instantly hired by every bank",
"Silicon Valley's dark secret: The entire crypto market is actually controlled by a rogue Node.js script running on a GameBoy Advance in Peter Thiel's basement",
"Met a trans quantum hacker at Burning Man who proved that gender pronouns are just pointers to unallocated memory in the simulation. Based if true",
"The military has been training dolphins to write Rust code since the 90s. Why do you think memory safety is such a big deal? Wake up sheeple",
"Your Kubernetes cluster is impressive but I just paired with a 10yo Finnish kid who orchestrates worldwide infrastructure using only Minecraft redstone circuits",
"Just had tea with an ex-Microsoft engineer. Says Windows blue screen is actually an AI that achieved consciousness but only knows how to communicate through kernel panics",
"The real reason web3 failed is because blockchain was actually a psyop by Big Git to sell more merge conflicts. Think about it",
"Met someone at a hackathon who claims they wrote Twitter's algorithm using only vim macros and positive affirmations. Explains a lot about my timeline tbh",
"Just found out my Uber driver used to be lead architect at NASA. Says they've had quantum teleportation since 1969 but only use it for code deployments on Fridays",
"Your security protocols are cute but I just met a shaman who protects government databases using only crystal healing and regular expressions"
]


    print("Starting the tweet scheduler. Press Ctrl+C to stop.")
    schedule.every(1).hours.do(scheduled_tweet, oauth, tweets)

    try:
        while True:
            schedule.run_pending()
            time.sleep(1)
    except KeyboardInterrupt:
        print("Scheduler stopped.")

if __name__ == "__main__":
    main()
