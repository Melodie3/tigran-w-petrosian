import discord
from dotenv import load_dotenv
from os import getenv
import random
import asyncio

# bot invite link: https://discord.com/api/oauth2/authorize?client_id=966474721619238972&permissions=274877910016&scope=bot

load_dotenv()
TOKEN = getenv('DISCORD_TOKEN')
OWNER_ID = int(getenv('OWNER_ID'))

intents = discord.Intents.default()
#intents.members = True
intents.messages = True
intents.reactions = True
#intents.guilds = True
intents.message_content = True

client = discord.Client(intents=intents, owner_id=OWNER_ID)

latent_dreamer_id = 973811353036927047

ignore_list = [760090287003140127, #petrosian bot
                latent_dreamer_id, #latent dreamer
                964847473531174922, #Nuts n bolts
                960869046323134514, #machine mind
                1029793702136254584] #bingo-bot

messages_sent = {} # Where it stores message ids and who triggered them. Anyone with a role in allowed_roles can delete any message regardless of whether it's in here or not.
message_limit = 1000  # The number of messages that'll be stored in messages_sent before it starts removing old ones.

allowed_roles = [ # These are the role ids for roles that can delete any Petrosian message, even if it isn't in messages_sent. You can comment these out to remove them.
    958755031820161025, # Admin
    958512048306815056, # Moderator
    1119445209923723396, # Deputized
    # 970549665055522850 # Trusted
]

allowed_role_names = [
    "admin",
    "administrator",
    "moderator",
    "mod",
    "deputized",
]

phrases_database = list([
    { 
        "keys" : ["pipi", 
                    "pampers", 
                    "tigran", 
                    "petrosian",
                    "always play fair",
                    "true will never die"] ,
        "responses" : ["Are you kidding ???",
                        "What the \*\*\*\* are you talking about man ?",
                        "You are a biggest looser i ever seen in my life !",
                        "You was doing PIPI in your pampers when i was beating players much more stronger then you!",
                        "You are not proffesional, because proffesionals knew how to lose and congratulate opponents, you are like a girl crying after i beat you!",
                        "Be brave, be honest to yourself and stop this trush talkings!!!",
                        "Everybody know that i am very good blitz player, i can win anyone in the world in single game!",
                        'And "w"esley "s"o is nobody for me',
                        "just a player who are crying every single time when loosing, ( remember what you say about Firouzja ) !!!",
                        "Stop playing with my name, i deserve to have a good name during whole my chess carrier",
                        "I am Officially inviting you to OTB blitz match with the Prize fund! Both of us will invest 5000$ and winner takes it all!",
                        "I suggest all other people who's intrested in this situation, just take a look at my results in 2016 and 2017 Blitz World championships, and that should be enough...",
                        "No need to listen for every crying babe, Tigran Petrosyan is always play Fair !",
                        "And if someone will continue Officially talk about me like that, we will meet in Court!",
                        "God bless with true!",
                        "True will never die !",
                        "Liers will kicked off..."],
        "index" : 0 
    },
    { "keys" : ["google en passant"] ,
        "latent_dreamer_wait" : 1,
        "responses" : ["holy hell!",
                        "Amazing. I did not know that, thank you. This is the game that keeps on giving.",
                        "Will do. Thank you buddy!",
                        "Thanks! *Dry humps your leg*",
                        "I don't do google bruh. Too many effects.",
                        "google gay porn",
                        "ok 😶", # Abstain Aphotian and Atramentous Ebony
                        "that's a bunch of crap",
                        "good idea why didnt i think of that",
                        "that's fucked. why??",
                        "Okay i didn't know about that one thats actually cool",
                        "LOOOOOOOOOOL\n\nOk, thanks dude! I realize now that I'm much noobier that I thought. I thought en passant was something similar, but not this.",
                        "I read it a long time ago and was mindblown",
                        "Sorry?",
                        "En passant? How do I spell that?",
                        "WTF is this wizardry",
                        "This is so offensive/inappropriate in so many ways I can't even begin to describe.", #GPT-3
                        "THAT SEEMS LIKE BULLSHIT BROTHER, BUT THANKS. LETS CRANK ON AWOOOOOOOGA",
                        "Haha, chess is interesting. Now I'm going to kill myself.",
                        "I don't speak Vatican my guy",
                        "wow that fixes everything now chess is the most amazing game ever because of this one thing that only happens in a rare circumstance wow thank you for fixing chess for me it is no longer a bore",
                        "Didnt want it",
                        "No. That sounds stupid",
                        "I'm not a chess guy, but I know the rules. I learned about en passant for the first time last year. Talked to people about it. Not everybody likes it. Some people think it's show-offy over complicated nonsense for mental masturbators with overgrown egos. They make the same kinds of remarks you've blusterociously buffoonificated about a punctuation mark. You've been acting like that thing shoved a rocket up your butt and killed your parents.",
                        "I know what en passant is dumbass you just blundered mate in one",
                        "Fuck off you dumb cunt",
                        "Fuck you.",
                        
                        "holy shit\nhtat sounds terrible",  #wishful
                        "i cant even read it\ni dont chess", #wishful

                        "Go fuck yourself. I'm going to scream.",
                        "man i can't even read that\nwhat the fuckgj",
                        "Oh yeah I heard that rule. The weird one with the pawns.",
                        "what the fuck\nstop hurting my brain\ni'm screwed!", #emptyRook
                        "explain en passant.",
                        "who you callin peasant bitch",
                        "Man I know what an en passant is, I just dont know whats happening in that board",
                        "im from anarchy chess too bro", #kapola7
                        "huh, til. What a smart gal", #zyia
                        "Learn chess lol",
                        "https://cdn.discordapp.com/attachments/958560322095046706/967861562775851129/IMG_9414.gif", #en passant gif
                        "i dont keep up with all the responses at this point\ntheres just so many",
                        "Filth pig go play dominoes because you have no idea about the tu art of chess",
                        "What is that\nA glitch?", #hickey Nickey
                        "I'm not gonna google some French fuck words", #piguy
                        "DIE DIE DIE DIE DIE DIE DIE DIE DIE DIE DIE DIE DIE DIE DIE DIE DIE DIE DIE DIE DIE DIE DIE DIE DIE DIE DIE DIE DIE DIE DIE DIE DIE DIE DIE DIE DIE DIE DIE DIE DIE DIE DIE DIE DIE DIE DIE DIE DIE DIE DIE DIE DIE DIE DIE DIE DIE DIE DIE DIE DIE DIE DIE DIE DIE DIE DIE DIE DIE DIE DIE DIE DIE DIE DIE DIE DIE DIE DIE DIE DIE DIE DIE DIE DIE DIE DIE DIE DIE DIE DIE DIE DIE DIE DIE DIE DIE DIE DIE DIE DIE DIE DIE DIE DIE DIE DIE DIE DIE DIE DIE DIE DIE DIE DIE DIE DIE DIE DIE DIE DIE DIE DIE DIE DIE DIE DIE DIE DIE DIE DIE DIE DIE DIE DIE DIE DIE DIE DIE DIE DIE DIE DIE DIE DIE DIE DIE DIE DIE DIE DIE DIE DIE DIE DIE DIE DIE DIE DIE DIE DIE DIE DIE DIE DIE DIE DIE DIE DIE DIE DIE DIE DIE DIE DIE DIE DIE DIE DIE DIE DIE DIE DIE DIE DIE DIE DIE DIE DIE DIE DIE", #Latent dreamer
                        "I dod\ndid" #ashley the traveler
                        "very original", #emily
                        "I already know what that is, have you considered googling your address and sending it to me?"
                        ], 
        "index" : 0,
    },
    { "keys" : ["hikaru",
                "don't care",
                "doesn't care"],
        "responses" : ["yes, if hikaru has million number of fans i am one of them. if hikaru has ten fans i am one of them. if hikaur has no fans. that means i am no more on the earth. if world against hikaur, i am against the world. i love hikuar till my last breath... die hard fan of hiraku. Hit like if u think kahiru best & smart in the world",
                        "https://www.youtube.com/watch?v=TaQ6ubWJ-LA",
                        "Yeah, it's just a draw. Yeah, I mean, it's just a draw. I mean, I offered him a draw before. I-I mean... I offered him a draw he offered to draw and I offer to draw, I mean, that's fine. I don't care because he offered a draw and I offered him one later. That's just bad sportsmanship I-I don't... I don't even care. Because he offered to draw and I offer- I offered a draw the very next half-move. Um, so... no, I mean, that's fine. He can take that but I don't care. I literally don't care... because there's certain things like flagging in a situation, but draws you don't do. [cuts out] offered it and he didn't - he didn't take it I mean that's fine. He wants to win like that, he can take it. I literally don't care",
                        """Greetings, Eric Hansen. It appears that while playing a game of speed chess, you have forced me to run out of time, thus making me "flag", or lose on time. In response, I shall declare that I have zero interest in your flagging, as it is of little to no importance to me."""],
        "index" : 0 
    },
    { "keys" : ["bing en passant"],
        "responses" : ["I will have to consult the board about this new development. Things weren't like this in my day. The rules don't consider such a wide variety of bone structures. Truly, the modern world is much more accepting then it was when I first created chess."],
        "index" : 0 
    },
    { "keys" : ["google gay porn"],
        "responses" : ['''"Your chess is insane." Hikaru said, as he slipped his feminine hand into Magnus's pants and smirked. "Are you trying to mate me?" protests Magnus, as Hikaru blushes, the boyish figure undressed before Magnus. "Weak tempo play, Hikaru." The two kissed, deeply and passionately, and afterwards Magnus places his Rook into Hikarus open line.''',
        '''"Checkmate." Hikaru's face contorts to a look of utter disbelief, as he falls onto the bed, defeated. "You're quite good at this." Hikaru says, rolling over and kissing Magnus on the neck. "A natural."\n"I should be, I was the world champion for a time." Magnus smirks and Hikaru's eyes widen.\n"You never told me that."\n"You never asked." ''',
        '''"I guess I should've known, you're just so good at everything." Hikaru said, admiring Magnus's body. "I bet you're good in bed too."\n"Why don't you find out?" Magnus said, as he pulled Hikaru close, the two kissing passionately as their bodies intertwined. There would be no chess match this time, only the game of love, and Magnus was determined to come out on top.''',
        '''The two chess players were in the midst of a passionate embrace when Hikaru's father, a grandmaster, walked in on them. "Hikaru, what are you doing?" he asked, "You're supposed to be studying!"\n"I am studying, Father," Hikaru replied, "I'm studying the most important thing of all: love."''',

        ],
        "index" : 0 
    },
    { "keys" : ["rook a4",
                "161660",
                "levy"],
        "responses" : ["Look, I saw Ra4, I just didn't like it.",
                        "This man had Rook a4, like, 3 moves in a row, didn’t even see it, like, when I see a queen come here, this is the first thing I think of.   Damn. Damn. Damn damn damn. Well, at least this player has “potato” in his name ’cause he played like a potato. He played like a potato.",
                        "1300 is this game, 1300. Uh, mid-1200 into 1300 is my final guess and here we go. 1660. 1660. You’re telling me a 1600 hung a piece on move 6?   You are telling me that a 1600 rated player hung a piece on move 6. 1600 rated player hung a piece on move 6. This guy is 1660 and he hung a piece on move 6. 16-16-60 and he hung a piece on move 6.  Didn’t see a trapped queen, could’ve trapped the man’s queen, didn’t trap the man’s queen, could’ve trapped the man’s queen.",
                        "16-16-60 and he hung a piece on move 6.  Didn’t see a trapped queen, could’ve trapped the man’s queen, didn’t trap the man’s queen, could’ve trapped the man’s queen.",
                        "<:levy_rozman:958754416654176266>",],
        "index" : 0 
    },
    { "keys" : ["portuguese",
                "brazil"],
        "responses" : ["Está de zoeira ???",
                        "Mas que \*\*\*\* você tá falando cara ?",
                        "Você é o maior perdedor que eu já vi na minha vida !",
                        "Você fazia PIPI nas fraldas enquanto eu vencia jogadores muito mais fortes do que você!",
                        "Você não é profissional, porque profissionais sabem perder e parabenizar os adversários, você parece uma menininha chorando depois de perder pra mim!",
                        "Seja corajoso, seja honesto contigo mesmo e pare de falar merda!!!",
                        "Todo mundo sabe que eu sou um ótimo jogador de blitz, posso vencer qualquer um no mundo em uma partida!",
                        '''E "w"esley "s"o não é ninguém pra mim, só um jogador que fica de mimimi toda vez que está perdendo, ( lembra o que falou do Firouzja ) !!!''',
                        "Para de zoar com minha imagem, eu sempre mereci respeito na minha carreira de xadrez, e estou oficialmente te convidando pra uma partida cara-a-cara de blitz pelo prêmio!",
                        "Nós dois vamos investir $5000 e o vencedor leva tudo!",
                        "Sugiro a todos os interessados na situação, que olhem os meus resultados nos campeonatos mundiais de Blitz em 2016 e 2017, isso já deve bastar...",
                        "Não precisa ficar escutando mimimi de bebês, Tigran Petrosian é sempre joga limpo !",
                        "E se alguém continuar a falar de mim assim oficialmente, eu te vejo no tribunal!",
                        "Deus abençoe a verdade!",
                        "A verdade nunca morre !",
                        "Mentirosos serão chutados..."],
        "index" : 0 
    },
    { "keys" : ["піпі"],
        "responses" : ["Ты издеваешься ???",
                        "О чем, черт возьми, ты говоришь, мужик?",
                        "Ты самый большой неудачник, которого я когда-либо видел в своей жизни!",
                        "Ты делал PIPI в своих памперсах, когда я побеждал игроков намного сильнее тебя!",
                        "Ты не профессионал, потому что профессионалы умели проигрывать и поздравлять соперников, ты как девочка плачешь после того, как я тебя обыграл!",
                        "Будь смелым, будь честным с собой и прекрати болтовню!!!",
                        "Все знают, что я очень хорошо играю в блиц, я могу победить кого угодно в мире в одиночной игре!",
                        '''А "w"esley"so для меня никто, просто игрок, который плачет каждый раз, когда проигрывает (помните, что вы говорите о Фируздже)!!!''',
                        "Хватит играть моим именем, я заслуживаю доброго имени на протяжении всей своей шахматной карьеры, Официально приглашаю вас на блиц-матч ОТБ с призовым фондом!",
                        "Мы оба вложим по 5000$, и победитель получит все!",
                        "Всем остальным, кого интересует эта ситуация, предлагаю просто взглянуть на мои результаты на чемпионатах мира по блицу 2016 и 2017 годов, и этого должно быть достаточно...",
                        "Не нужно выслушивать каждого плачущего младенца, Тигран Петросян всегда играет по-честному!",
                        "И если кто-то продолжит Официально обо мне так говорить, встретимся в суде!",
                        "Дай бог с правдой!",
                        "Правда никогда не умрет!",
                        "Лжи начнутся..."],
        "index" : 0 
    },
    { "keys" : ["russian", "ukraine"],
        "responses" : ["Слава Україні! :flag_ua:",
                        "Slava Ukraini! :flag_ua:"],
        "index" : 0 
    },
    { "keys" : ["garry chess",
                "nft"],
        "responses" : ["""Garry, how do you want to be remembered?" I admit I thought about such things even as a young world champion, but back then I only considered a legacy at the chessboard. Decades later, this third drop of NFTs is my answer.""",
                        "I have an announcement to make. I have created chess amended. It’s sort of like chess except without en passant. I think it makes for a more fair and balanced game.",
                        "I had no choice. The Big Pipi unions were relentless. Big Brick is slightly less impressed but you can’t please everyone. I’ve suggested they start up a market in building and infrastructure instead. They have taken it under advisement."],
        "index" : 0 
    },
    { "keys" : ["chess 2"],
        "latent_dreamer_wait" : 1,
        "responses" : ["That sounds like a good idea. I should go and invent that.",
                        "It's a french chess game.",
                        "It takes place in a house and the pieces are all different colours, they can move in any direction.",
                        "You move pieces in a random order, each move brings about a different outcome.",
                        "What can I say? A mind like mine is always thinking"],
        "index" : 0 
    },
    { "keys" : ["chess 3"],
        "responses" : ["I have an announcement to make.",
                        "I have created chess amended.",
                        "It’s sort of like chess except without en passant.",
                        "I think it makes for a more fair and balanced game."],
        "index" : 0 
    },
    { "keys" : ["duck duck go",
                "duckduckgo"],
        "responses" : ["What the fuck is duck duck go"],
        "index" : 0 
    },
    { "keys" : ["yahoo"],
        "responses" : ["What the fuck is yahoo"],
        "index" : 0 
    },
    # { "keys" : ["pornhub en passant"],
    #     "responses" : ["<:why:959245770119319593>",
    #                     "<:whytf:959327131219947541>"],
    #     "index" : 0 
    # },
    { "keys" : ["horse move",
                "horsey",
                "horsie"],
        "latent_dreamer_wait" : 1,
        "responses" : ["The knight moves unconventionally compared to other chess pieces.",
                        "Whereas other pieces move in straight lines, knights move in an “L-shape” ",
                        "—that is, they can move two squares in any direction vertically followed by one square horizontally, or two squares in any direction horizontally followed by one square vertically.",
                        "The Horsey moves along the two adjacent sides of the right angle of a triangle with a hypotenuse of √5",
                        "<:horsey:960727531592511578>"],
        "index" : 0 
    },
    # { "keys" : ["bobby",
    #             "fischer",
    #             "fisher"],
    #     "responses" : ['''"They're terrible chess players... I guess they're just not so smart... I don't think they should mess into intellectual affairs, they should keep strictly to the home" - Bobby Fischer''',
    #                     '''"They're all weak, all women. They're stupid compared to men. They shouldn't play chess, you know. They're like beginners. They lose every single game against a man. There isn't a woman player in the world I can't give knight-odds to and still beat." - Bobby Fischer''',
    #                     '''"It's the fault of the chess players themselves. I don't know what they used to be, but now they're not the most gentlemanly group. When it was a game played by the aristocrats it had more like you know dignity to it. When they used to have the clubs, like no women were allowed and everybody went in dressed in a suit, a tie, like gentlemen, you know. Now, kids come running in their sneakers. Even in the best chess club-and they got women in there. It's a social place and people are making noise, it's a madhouse." - Bobby Fischer''',
    #                     '''"She'll never beat any top men regularly - no woman can, They can't concentrate, they don't have stamina and they aren't creative. They're all fish." - Bobby Fischer''',
    #                     '''"Yes this is all wonderful news, it is time that the fucking Jews get their heads kicked in. It's time to finish off the US once and for all." - Bobby Fischer''',
    #                     '''"...Everybody knows how you ... how you.. I was happy, could not really believe what has happened. I just cant be crying about the US , you know ..All the crimes the US is committing all over the world." - Bobby Fischer''',
    #                     '''"This just shows, what goes around, that comes around even to the United States. Thats what happened tonight, what goes around comes around even to the United States." - Bobby Fischer'''],
    #     "index" : 0 
    # },
    # tagalog pipi
    { "keys" : ["Philippines",
                "tagalog",
                "Iyakin", 
                "Pro geymer",
                "pro gamer",
                "Congrats",
                "Trastok",
                "Pinakamagaling",
                "Gago",
                "Desurb",
                "Dasurb",
                "Pustahan",
                "Totoo",
                "Sinungaling"],
        "responses" : ["Nagbibiro ka ba ??? Ano pinagsasabi mong pu** ina ka ?",
                        "Ikaw yung pinakagaggong nakalaro ko sa buong buhay ko !",
                        "Nagpi-PIPI ka pa sa pampers mo nung tumatalo nako ng mga taong mas malakas pa sayo!",
                        "Di ka pro geymer, kasi mga pro geymer alam na pag natalo i-congatulaet mga kalaban, ikaw iyakin ka parang babae pag tinalo kita!",
                        "Magmatapang ka, magtotoo ka sa sarili at wag mo ko ma trastok trastok jan!!!",
                        "Alam ng lahat na ako pinakamagaling na blitz player, kaya ko talunin lahat sa buong mundo sa isang laro lang!",
                        '''Tas yang si "w"esley "s"o wala lang yang gagong yan, iyakin yan pag natalo yan, ( tandaan niyo sinasabi niyo kay Firouzja ) !!!''',
                        "Wag niyo paglaruan pangalan ko, desurb ko malinis na pangalan sa buong chess career ko, iniinvite kita sa OTB blitz game na may Prize fund! Pustahan tayo $5000 manalo kunin lahat!",
                        "Suggest ko lahat ng interesado sa sitwasyon na to, tignan niyo lang mga resulta ko sa 2016 at 2017 blitz world championship sapat na siguro yon...",
                        "Di na kelangan pakingaan lahat ng mga iyaking babe, laging patas laro ni Tigran Petrosyan !",
                        "At pag may manggugulo pa ng pangalan ko, magkita tayo sa korte!",
                        "God bless with true! Di mamamatay ang totoo ! Mga sinungaling alisin... "],
        "index" : 0 
    },
    # greek pipi
    { "keys" : ["greek", "malaka", "greece"],
        "responses" : ["Πλάκα κάνεις ???",
                        "Για τι \*\*\*\* λες ρε φίλε; Είσαι ο μεγαλύτερος χαμένος που έχω δει ποτέ στη ζωή μου!",
                        "Έκανες PIPI στα pampers σου όταν κέρδιζα παίκτες πολύ πιο δυνατούς από εσένα!",
                        "Δεν είσαι επαγγελματίας, γιατί οι επαγγελματίες ξέρουν να χάνουν και να συγχαίρουν τους αντιπάλους, είσαι σαν ένα κορίτσι που κλαίει αφού σε κέρδισα!",
                        "Να είσαι γενναίος, να είσαι ειλικρινής με τον εαυτό σου και να σταματήσεις αυτές τις αστείες κουβέντες!!!",
                        "Όλοι γνωρίζουν ότι είμαι πολύ καλός παίκτης blitz, μπορώ να κερδίσω οποιονδήποτε στον κόσμο σε ένα παιχνίδι!",
                        '''Και ο "w"esley "s"o δεν είναι κανένας για μένα, απλά ένας παίκτης που κλαίει κάθε φορά όταν χάνει, (θυμήσου τι έλεγες για τον Firouzja) !!!''',
                        "Σταμάτα να παίζεις με το όνομά μου, αξίζω να έχω καλό όνομα σε όλη τη διάρκεια της καριέρας μου, σε προσκαλώ επίσημα στον αγώνα blitz OTB με το ταμείο επάθλων!",
                        "Και οι δύο θα επενδύσουμε 5000$ και ο νικητής τα παίρνει όλα!",
                        "Προτείνω σε όλους τους άλλους ανθρώπους που ενδιαφέρονται για αυτήν την κατάσταση, απλώς ρίξτε μια ματιά στα αποτελέσματά μου στο Παγκόσμιο Πρωτάθλημα Blitz του 2016 και του 2017, και αυτό θα είναι αρκετό...",
                        "Δεν χρειάζεται να ακούτε για κάθε μωρό που κλαίει, ο Tigran Petrosyan παίζει πάντα δίκαια!",
                        "Και αν κάποιος συνεχίσει επίσημα να μιλάει για μένα έτσι, θα βρεθούμε στο δικαστήριο!",
                        "Ο Θεός να ευλογεί με την αλήθεια!",
                        "Η αλήθεια δεν θα πεθάνει ποτέ!",
                        "Οι ψεύτες θα ξεκινήσουν..."],
        "index" : 0 
    },
    { "keys" : ["spanish",
                "espanol",
                "español",
                "inquisition"],
        "responses" : ["Estás bromeando ???",
                        "¿De qué demonios estás hablando hombre?",
                        "¡Eres el perdedor más grande que he visto en mi vida!",
                        "¡Estabas haciendo PIPI en tus mimos cuando yo vencía a jugadores mucho más fuertes que tú!",
                        "No eres un profesional, porque los profesionales sabían perder y felicitar a los oponentes, ¡eres como una niña que llora después de que te gane!",
                        "¡¡¡Sé valiente, sé honesto contigo mismo y deja de hablar de esta tontería !!!",
                        "Todo el mundo sabe que soy muy buen jugador de blitz, ¡puedo ganar a cualquiera en el mundo en un solo juego!",
                        '''Y "w" esley "s" o no es nadie para mí, solo un jugador que está llorando cada vez que pierde, (recuerda lo que dices sobre Firouzja) !!!''',
                        "Deja de jugar con mi nombre, merezco tener un buen nombre durante toda mi carrera de ajedrez, ¡te estoy invitando oficialmente a la partida relámpago OTB con el fondo de premios!",
                        "¡Ambos invertiremos 5000 $ y el ganador se lo lleva todo!",
                        "Sugiero a todas las demás personas interesadas en esta situación, que solo echen un vistazo a mis resultados en los campeonatos mundiales Blitz de 2016 y 2017, y eso debería ser suficiente ... ¡No hay necesidad de escuchar a todos los bebés que lloran, Tigran Petrosyan siempre juega limpio!",
                        "Y si alguien sigue hablando oficialmente de mí así, ¡nos veremos en la Corte! ",
                        "Dios los bendiga con la verdad! ¡La verdad nunca morirá! Mentirosos arrancará ..."],
        "index" : 0 
    },
    { "keys" : ["french",
                "baguette"],
        "responses" : ["Please censor fr\*nch, this is a family server.",
                        "Whoa buddy! Do you speak to your family with those words?",
                        "I'm not gonna warn you again!",
                        "Qu’est-ce que tu viens juste de dire sur moi petite salope ?",
                        "je te ferais savoir que je suis sorti premier de ma classe dans la légion étrangère, et j’ai participé à de nombreuses attaques surprises contre Al-Quaeda, j’ai plus de 300 victimes confirmées.",
                        "Je suis entrainé aux tactiques de gorilla et je suis le meilleur sniper de toutes les forces armées françaises.",
                        "Tu n’es rien de plus qu’une autre cible. Je te ferais disparaitre de cette putain de planète avec une précision jamais-vue auparavant, souviens-toi de mes putains de paroles.",
                        "Tu peux pense que tu peux t’en sortir après avoir dit de la merde sur moi sur Intemet? Réfléchis-bien, enculé.",
                        "Au moment où nous parlons je contacte mon réseau d’espions à travers le globe et ton IP se fait tracer en ce moment même alors prépare toi à la tempête, vermine.",
                        "La tempête qui va balayer cette pathétique petite chose que tu appelles ta vie. T’es putain de mort gamin.",
                        "Je peux être n’importe où, n’importe quand, et je peux te tuer de plus de sept-cent manières, et cela juste à mains nues.",
                        "Je suis non seulement très entrainé au combat à main nue, mais j’ai aussi accès à l’arsenal entier de l’Armée de Terre de la République et je l’utiliserai à son maximum pour rayer ton petit cul du continent, espèce de petite merde.",
                        "Si seulement tu avais su la vengeance impie qui t’attendait grâce à ton petit commentaire « malin », peut être tu aurais fermé ta gueule.Mais tu ne l’a pas fait, non tu ne l’a pas fait, et maintenant tu en paye le prix, putain d’abruti.",
                        "Je vais te chier dessus jusqu’à ce que tu te noies dedans. T’es putain de mort, gamin.",
                        "Est-ce que tu me niases? De quoi tu parles mec?",
                        "T’es le plus gros looser j’ai jamais vu de ma vie!",
                        "Tu faisais PIPI dans tes pampers quand je battais des joueurs beaucoup plus plus forts que toi!",
                        "Tu n’es pas proffesionel, parce que les proffesionels savaient comment perdre et féliciter des adversaires, tu es comme une fille pleurant après que je te batte!",
                        "Sois brave, sois honnête à toi-même et arrête de dire n’importe quoi!!!",
                        "Tout le monde sais que je suis très bon joueur blitz, je peux gagner n’importe qui dans le monde en seule partie! Et «w»esley «s»o n’est personne pour moi, just un jouer qui es pleurant chaque fois en perdant, (souviens-toi de ce que tu dis à propos de Firouzja) !!!",
                        "Arrête de jouer avec mon nom, je mérite un bon nom durant ma toute carreère d’échecs, je d’invite Officiellement au match OTB blitz avec le fonds Prix! Chacun de nous investit 5000$ et gagnant prend tout!",
                        "Je suggère tous les autres personnes quisont intéressés dans la situation, juste regardez mes résultats aux championnats du monde Blitz 2016 et 2017, et ça devrait être assez…",
                        "Pas besoin d’écouter chaque à pleurage babe, Tigran Petrosyan est toujours joueur juste!",
                        "Et si quelqu’un va continuer Officiellement parler de moi comme ça, nous nous rencontrerons en Cour!",
                        "Dieu bénit avec vrai! Vrai ne mourra jamais! Les mentures vont est lancés…",
                        "DE QUOI TU PARLES, **MEC??**",
                        "ESPÈCE DE PUTE AUX OS FRAGILES !! tu devrais même pas jouer aux échecs, tu pourrais casser un os juste en essayant de prendre une pièce.",
                        "QUOI ?!!! mange juste un peu de pein espèce d’idiot. connais tu meme la beuté du pein?? met le juste dans ta bouche et mastique le, Laisse l’Amylase décomposer les glucides et former du sucre, attend que le goût soit senti par ta langue, puis les nerfs l’envoyant à ton cerveau  . . . le cerveau allumant ensuite ton système de Récompense, te faisant sentir de l’exceptionnel plaisir du pein.",
                        ],
        "index" : 0 
    },
    { "keys" : ["scholar's mate",
                "scholars mate"],
        "responses" : ["I know what scholars mate is dumbass, you just blundered mate in 4"],
        "index" : 0 
    },
    { "keys" : ["breadchess",
                "bread random chess"],
        "responses" : ["That is a lot of words. I can't read. However I shall allow this bread of chess to be played by my loyal followers.",
                        "WHAT ?!!! just eat some bredd you idiot. do u even know the beuty of bredd?? just put it in your mouth and chew it, Let the Amylase breakdown the carbohydrates and form sugar, wait for the taste to be sensed by your tongue, then the nerves sending to your brain  . . . the brain then turning on your Reward system, making you feel amazing bredd pleasure.",
                        ],
        "index" : 0 
    },
    { "keys" : ["bone",
                "brittle",
                "broken"],
        "responses" : ["YOU BRITTLE BONED BITCH !! you shoudnt even play chess, as you may break a bone just trying to pick up a piece"],
        "index" : 0 
    },
    { "keys" : ["math",
                "cringe"],
        "responses" : ["WHAT?!!!",
                        "Maths is beuty , maths is GOD maths is UNIVERSE, maths is EVERYTHING.", 
                        "Dont you dare call maths cringe. Without matha we wouldn't have had all this technological development and shit.", 
                        "The world is beutiful only thanks to maths. Do you even know how many ways maths can be used to help us in real life? you are a dumb, worthless, brainless, nincompoop who can be easily nonplussed. you don't even deserve to live in this beutiful maths filled world." ,
                        "Now mathematics is both a body of truth and a special language, a language more carefully defined and more highly abstracted than our ordinary medium of thought and expression. Also it differs from ordinary languages in this important particular: it is subject to rules of manipulation. ",
                        "Once a statement is cast into mathematical form it may be manipulated in accordance with these rules and every configuration of the symbols will represent facts in harmony with and dependent on those contained in the original statement. ",
                        "Now this comes very close to what we conceive the action of the brain structures to be in performing intellectual acts with the symbols of ordinary language. ",
                        "In a sense, therefore, the mathematician has been able to perfect a device through which a part of the labor of logical thought is carried on outside the central nervous system with only that supervision which is requisite to manipulate the symbols in accordance with the rules.",
                        ],
        "index" : 0,
        "response ratio" : 0.5 
    },
    { "keys" : ["clean"],
        "responses" : ["I am clean"],
        "index" : 0 
    },
    { "keys" : ["sus",
                "amongus",
                "among us",
                "amogus"],
        "responses" : ["<:sus:961517169424883722>"],
        "index" : 0 
    },
    { "keys" : ["outstanding move"],
        "responses" : ["https://cdn.discordapp.com/attachments/960884493663756317/977470589646282842/6gz6cm.jpg"],
        "index" : 0 
    },
    { "keys" : ["i am the senate"],
        "responses" : ["https://static.wikia.nocookie.net/star-wars-memes/images/1/10/6C8F4484-9D35-4219-B9C0-7A830BB1E353.jpeg/revision/latest?cb=20200415193930"],
        "index" : 0 
    },
    { "keys" : ["o-o",
                "0-0",
                "castle"],
        "responses" : ["""*notices rook* "O-O, what's this?" *castles kingside*"""],
        "index" : 0 
    },
    { "keys" : ["copypasta"],
        "responses" : ["""You're pasting your own copy pasta too much. Do you think you're that important that YOUR copy pasta needs to be shared with everyone? I can't believe your hubris, WE the public will decide if your copy pasta is worthy or not to be copied and pasted all over the world wide web. I bet you even decline en passants and DEFLECT the brick because you think you're above the law. I hope you learn from this and refrain from copypasta-ing your own copypastas in the future.""",
                        """it'll come naturally, one cant just sit down there and think just to write a copypasta. Writing copypastas are hard and cannot be mastered by everyone. Not all long pieces of text are copypastas and similarly not all copypastas need to be long, but the longer the copypasta  . . .the better it'll be. Any long text comes from the heart. Thinking and planning to write long texts will never be good as the natural flow of typing from the heart. For example, this is a long piece of text. Its not insanely huge, but has a decent length. But is this a copypasta? maybe . . . maybe not., But it came naturally, not by planning""",
                        """ENGINE pathetic Turn off your ENGINE and play cheat codes for what? intnernet points? OUCH Look at how BAD you are oh and to boot? your’e a CHEATER Nice L I F E = pathetic Seriously look at how BAD you are at chess want to konw why? Because you spent your time cheating instead of learning Now what do you get out of chess? you can’t play it well at all I wiped your board embarrassed your game simply because I never even thought about cheating you’re a double loser enjoy that low self esteem what a loser Look at the disparity bettween YOUR game and this that’s it just sit there knowing you have to cheat to get what again? Oh right - meaningless “low self esteem” points on the internet LMAO flagged me??? Exactly HOW??? I WIPED your bord Dude...CHEAT some more bro !!!! pathetic I WIPED YOUR board you can’t compete unless you CHEAT dude are you seriously going to try that/???? derp derp duhhhh “2-1” I know what cheat codes look like And we both know y9ou’re turning on your engine to avoid detection BOTH games then explain the disparity in play between the games dude SHUT UP it’s only going to get MORE embarrassing for you Explain the disparity in YOUR skill level you’re really a loser for having to CHEAT at chess tell me what you get out of it I’m not angry I’m just sitting here callling you out it’s pathetic yes you are. so stop eplain the disparity in your OWN skill levle Moron == when you start to lose, you turn on your cheating engine just moronic No - you’re just trying to deny it Let me guess - Trump voter?? explain the disparity in skill level then of your OWN game I’ve now asked you 4x.....funny how you avoid talking about that""",
                        """Oh wait. I struck a cord Moron Chess Player = Moron Trump voter MORON just STOP you REFUSE to answer the basics Why??? Becuase you CHEAT Because you’re a LOSER who doesn’t reallize That when you cheat it’s so obvious that you can’t defend yourself Explain the disparity in your skill level from game to game youre’ NOT better than me your ENGINE is your CHEAT CODE is YOU are not better than me YOU are the loser who CHEATS at chess end of story LMO what are we at now? 5-6X???? Effin TRUMP VOTER BAnd of Idiots you ACT like one you have ZERO integrity you hvae ZERO credibility you lie like a rug And you cheat like a toddler you call me out about how I “act” when you CHEAT!! Jesus but you do EXplain the disparity in your OWN skill levle DO IT!!! I cleared your board didn’t t? BRO - moron!!! 11x I’ve asked you to explain the disparity in your OWN skill level 11x you REFUSEE to even acknowledge it = CHEATER MORON LIttle girl can’t lose is your self esteem THAT fragile???? is it?? Little baby of a man that you can’t even lose an anonymous game online to a total stranger??? Are you such a waste of space that you have to cheat at chess? you cheaters are just utter LOSERS I’m calling you what you are- a LOSER because you cheat at chess""",
                        """You are a sick idiot! Get treatment, crazy. Clown, nameless. Look at your rating. You absolutely do not know how to play. You also talk nonsense with your broomstick. Match with you? What about you??? What’s your name? Nothing, crazy.""",
                        """Are you kidding ??? What the **** are you talking about man ? You are a biggest looser i ever seen in my life ! You was doing PIPI in your pampers when i was beating players much more stronger then you! You are not proffesional, because proffesionals knew how to lose and congratulate opponents, you are like a girl crying after i beat you! Be brave, be honest to yourself and stop this trush talkings!!! Everybody know that i am very good blitz player, i can win anyone in the world in single game! And "w"esley "s"o is nobody for me, just a player who are crying every single time when loosing, ( remember what you say about Firouzja ) !!! Stop playing with my name, i deserve to have a good name during whole my chess carrier, I am Officially inviting you to OTB blitz match with the Prize fund! Both of us will invest 5000$ and winner takes it all!\n\nI suggest all other people who's intrested in this situation, just take a look at my results in 2016 and 2017 Blitz World championships, and that should be enough... No need to listen for every crying babe, Tigran Petrosyan is always play Fair ! And if someone will continue Officially talk about me like that, we will meet in Court! God bless with true! True will never die ! Liers will kicked off...""",
                        "WHAT?!!! Maths is beuty , maths is GOD maths is UNIVERSE, maths is EVERYTHING. Dont you dare call maths cringe. Without matha we wouldn't have had all this technological development and shit. The world is beutiful only thanks to maths. Do you even know how many ways maths can be used to help us in real life? you are a dumb, worthless, brainless, nincompoop who can be easily nonplussed. you don't even deserve to live in this beutiful maths filled world.",
                        """WHAT ?!!! just eat some bredd you idiot. do u even know the beuty of bredd?? just put it in your mouth and chew it, Let the Amylase breakdown the carbohydrates and form sugar, wait for the taste to be sensed by your tongue, then the nerves sending to your brain  . . . the brain then turning on your Reward system, making you feel amazing bredd pleasure.""",
                        """Capybaras are great. They are giant cavy rodents native to South America. Tis' also the largest rodent, which is a very cool fact. They have such a lovely barrel shaped body and nice short head, which looks very. . . "Alluring". They look as if they are Angels sent by gods, but dont be fooled, for they are gods themselves. Anyone who disrespects a Capybara will be punished by their pipis not being bricked, but by their pipis becoming bricks. Therefore, i would like to conclude my speech and advice all of you to religiously pray The Almighty Capybaras.""",
                        """I can't fucking believe this, I can't fuckign believe this, what are you doing how did you win ??? I'm the one whos supposed to wun you plebian, you stupid uneducated scholar's matr pleb you, how did you win you don't enen know how the ohrsey moves i swear to god I'll fucking beat you next tine how about you stop being s o smug huh???""",
                        """I beat you like a dog ! You're my slave :)\nSee ya now looser :) Go crying to your mum skirt Oh no you're an orphan you can't !\nHAHAHAHAHAHAH FRANCE RULES !!!! Fat amercian you make me laugh\nand you're so mad ! FLawless victory for me\nSE YAAAAAAAAAAA\nkiss <3 :D :) :) :) :) =) :) :) =) :) :) =) :) :) =) =) =) =) :) ;) ;) :) ;) ;) ;) ;) ;) ;) ;) ;) ;) ;) ;) ;) ) ) ) D) A ;) ;) ;) ) ;) ;) ) ) ) a a )""",
                        """listen here you toe eyed cabbage, I didn’t come into this world to hear your swaggle ahh PERSON  =IDIOT mouth say IDIOT insults from an IDIOT like you, nice C R O O K E D    L E F T     T O E, your toe looks just like your stpiud IDIOT face, you probably DNOT even KNOW how to do 2+3 you IDIOT bald IDIOT person, I BET you typed this on your NOKIA phone, IDIOT""",
                        """This exquisitely illustrates the mindset that is plagueing the American man. Rather than actually trying to reach this concept of ‘perfection' himself, GothamChess instead resigns himself to simply praising and talking about the achievements of others. This ‘observer' mindset is what is causing the gradual, silent decline of our nation. America is the worlds most influential trading partner, and we cannot afford to lose our position as a global investor, but sadly this is what is happening due to the passivist nature of our citizens. The world will not look upon America favorably if we continue to be seen as a nation of whinhing, passive snowflakes. I understand this is a bit unrelated to the video, but i just need to let out some of the frustration that has been building up. Chess is a perfect example of what is happening, as we've even gone to the point of inventing machines to play the game for us, so we dont even have to put any effort in, and can simply sit back and enjoy the show. Levy Rosmann is a representative of this whole group of commentary channels that waste their lives simply on observing the achievements of more taltented people, a defective man. I hope that one day that America will look back at us in shame, and wish they descended from a nation of innovators and inventors, but I'm afraid there will be nobody left to look back.""",
                        """I cannot believe how incredibly stupid you are. I mean rock-hard stupid. Dehydrated-rock-hard stupid. Stupid so stupid that it goes way beyond the stupid we know into a whole different dimension of stupid. You are trans-stupid stupid. Meta-stupid. Stupid collapsed on itself so far that even the neutrons have collapsed. Stupid gotten so dense that no intellect can escape. Singularity stupid. Blazing hot mid-day sun on Mercury stupid. You emit more stupid in one second than our entire galaxy emits in a year. Quasar stupid. Your writing has to be a troll. Nothing in our universe can really be this stupid. Perhaps this is some primordial fragment from the original big bang of stupid. Some pure essence of a stupid so uncontaminated by anything else as to be beyond the laws of physics that we know. I'm sorry. I can't go on. This is an epiphany of stupid for me. After this, you may not hear from me again for a while. I don't have enough strength left to deride your ignorant questions and half baked comments about unimportant trivia, or any of the rest of this drivel. Duh.\n\nMaybe later in life, after you have learned to read, write, spell, and count, you will have more success. True, these are rudimentary skills that many of us "normal" people take for granted that everyone has an easy time of mastering. But we sometimes forget that there are "challenged" persons in this world who find these things more difficult. I wish you the best of luck in the emotional, and social struggles that seem to be placing such a demand on you.""",
                        """Now mathematics is both a body of truth and a special language, a language more carefully defined and more highly abstracted than our ordinary medium of thought and expression. Also it differs from ordinary languages in this important particular: it is subject to rules of manipulation. Once a statement is cast into mathematical form it may be manipulated in accordance with these rules and every configuration of the symbols will represent facts in harmony with and dependent on those contained in the original statement. Now this comes very close to what we conceive the action of the brain structures to be in performing intellectual acts with the symbols of ordinary language. In a sense, therefore, the mathematician has been able to perfect a device through which a part of the labor of logical thought is carried on outside the central nervous system with only that supervision which is requisite to manipulate the symbols in accordance with the rules.""",
                        """*Takes deep breath*\nYou see, every mornign, when I wake up, I find HUNDREDS, if not THOUSANDS of mesages in this chanel. Every time I go awya for THIRTY FUCKING MINUTES there are like FIVE HUNRED MESSAGES. And then sometimes I don’t even have the time to read everything and there’s alreayd more!!!!!!!!!!! Do yuo realy think I have the brainpower to memorise eveyrthing? No, that is not the case… stop talking of me like this and talking i am a someone who can’t remember eveything! I am just a normal human!!! So stop this trush talkings and get outa her!!!!!!!!!!""",
                        """holy fucking shit. if i see ONE more en passant meme i'm going to chop my fucking balls off. holy shit it is actually impressive how incredibly unfunny the entire sub is. it's not that complicated, REPEATING THE SAME FUCKING JOKE OVER AND OVER AGAIN DOES NOT MAKE IT FUNNIER. this stupid fucking meme has been milked to fucking death IT'S NOT FUNNIER THE 973RD TIME YOU MAKE THE EXACT SAME FUCKING JOKE. WHAT'S EVEN THE JOKE?????? IT'S JUST "haha it's the funne move from chess" STOP. and the WORST part is that en passant was actually funny for like a few years and it got fucking ruined in like a week because EVERYONE POSTED THE EXACT SAME FUCKING JOKE OVER AND OVER AGAIN. PLEASE MAKE IT STOP. SEEING ALL YOUR SHITTY MEMES IS ACTUAL FUCKING MENTAL TORTURE YOU ALL ARE NOT FUNNY. COME UP WITH A DIFFERENT FUCKING JOKE PLEASE""",
                        """Oh nice and emoji. And what do you expect to do with it, motherfucker? You replying with an emoji means that you have no idea what to say and have no valid argument. Go on. Use another one. Lets see how pathetic you guys are.""",
                        """There’s something satisfying about the resistant nature of the Lego piece. It stays together quite well despite my attempts to bite it with my front teeth. However when I move it to the back of my mouth and chomp with my back teeth, I have to apply some force. But there’s this satisfying sensation that is only felt once the Lego piece breaks from the force of my back teeth, and reshapes into a more digestible form. To then crunch down on these Lego fragments and break down the rest of the remaining shards, only extends my satisfaction. Then to swallow and feel the lego fragments in my throat, and to digest them, is a feeling indescribable by words.""",
                        ],
        "index" : 0 
    },
    { "keys" : ["capybara"],
        "responses" : ["""Capybaras are great.""",
                        """They are giant cavy rodents native to South America.""",
                        """Tis' also the largest rodent, which is a very cool fact.""",
                        """They have such a lovely barrel shaped body and nice short head, which looks very. . . "Alluring".""",
                        """They look as if they are Angels sent by gods, but dont be fooled, for they are gods themselves.""",
                        """Anyone who disrespects a Capybara will be punished by their pipis not being bricked, but by their pipis becoming bricks.""",
                        """Therefore, i would like to conclude my speech and advice all of you to religiously pray The Almighty Capybaras.""",
                        ],
        "index" : 0 
    },
    {
        "keys" : ["hans", "niemann"],
        "responses" : ["""I am not crazy! I know he had access to my preparation. I knew it. As if I could ever make such a mistake. Never. Never! I just - I just couldn't prove it. He covered his tracks, he got that idiot at the security check to lie for him. You think this is something? You think this is bad? This? This chicanery? He's done worse. That victory! Are you telling me that a man just happens to win like that? No! He orchestrated it! Hans! He got banned by chess.com! And I saved him! And I shouldn't have. I took him into my own company! What was I thinking? He'll never change. He'll never change! Ever since he was 9, always the same! Couldn't keep his hands out of the chess engine! But not our Hans! Couldn't be precious Hans! Cheating them blind! And HE gets to be a chess player? What a sick joke! I should've stopped him when I had the chance! ...And you, you have to stop him! You""",
                        """The real answer is actualy elementary. Magnus cheats. He's always had anal beads up his butt, maybe for the past 10 years. That's how he's been dominating the entire field of players. There was a slight dip during the time he played Caruana because he was so drunk he couldnt feel the vibrations well and ended up losinga game. His team decided to turn up the vibrations to max and that's how Magnus survived the encounter.""",
                        """Recently Magnus realized the anal bead supercomputer design he created had been stolen. Of course he couldn't come clean about cheating, so he drummed up the excuse of being bored so he wouldn't lose the World Championships to Nepo, who he suspects to have stolen the anal bead design after being humiliated in their prior contest. Magnus' suspicions were further evidenced by Nepo's performance during the Candidates. As u/GothamChess said, however, success is addictive, and Magnus decided to aim for 2900 before retiring for good.""",
                        """Little did he know, the real thief was the cocky supervillain Hans. Hans employed the anal bead tactic against Magnus. Being new to use the device, however, Hans didn't know that the signals he sent from his beads interfered with Magnus' device. Magnus feels unprompted vibrations on his prostate and realizes Hans stole his poopchute stockfish but couldn't use his own to retaliate lest Hans knew he was the true inventor of the device. That's why Magnus was uncharacteristically prone to inaccuracies and proceeded to lose the game.""",
                        """Afterwards, Magnus withdrew from the tournament, but not before putting out a vague tweet. While everyone interpreted it as Hans cheating, in reality, Magnus was also cheating but can't release definite proof since he'd also be in "big trouble".""",
                        """Case solved.""",
                        """Notorious for his inability to cope with defeat, Carlsen snapped. Enraged that the young Niemann, fully 12 years his junior, dared to disrespect the “King of Chess,” and fearful that the young prodigy would further blemish his multi-million dollar brand by beating him again, Carlsen viciously and maliciously retaliated against Niemann by falsely accusing Niemann."""
        ],              
        "index" : 0
    },
    {
        "keys" : ["messages", "unread"],
        "responses" : [
            "*Takes deep breath*",
            "You see, every mornign, when I wake up, I find HUNDREDS, if not THOUSANDS of mesages in this chanel. ",
            "Every time I go awya for THIRTY FUCKING MINUTES there are like FIVE HUNRED MESSAGES. ",
            "And then sometimes I don’t even have the time to read everything and there’s alreayd more!!!!!!!!!!! ",
            "Do yuo realy think I have the brainpower to memorise eveyrthing? No, that is not the case… stop talking of me like this and talking i am a someone who can’t remember eveything! ",
            "I am just a normal human!!! So stop this trush talkings and get outa her!!!!!!!!!!",
        ],
        "index" : 0
    },
    {
        "keys" : ["ghomerl vs cmauhin", "ghomerl vs. cmauhin", "ghomerl v cmauhin", "ghomerl v. cmauhin"],
        "responses" : [
            "No. fucking no. You can't just throw some random bullshit up here expecting everyone to get it. I demand answers right now and so fucking help me to whoever replies ghomerl vs cmauhin, fold yourself into a pretzel and eat your own ass",
            "Why is everyone talking about ghomerl and cmauhin, and what's with the pretzel comment? What is this?",
            "i want to ask what this means but i know everyone is just gonna say ghomerl vs. cmauhin",
            "I don’t know what’s happening but I’m just upvoting everything",
            "The fact that this is an actual mate in 2, with no fake pieces (other than the cool customized kings), and includes en pessant is awesome",
            "all I can think about are ghomerl and cmauhin. I haven’t eaten or slept in days. It’s live they’ve invaded my mind, every time I try to think about something else, I experience the most excruciating headache. Somebody help me. ghomerl vs cmauhin. ghomerl vs cmauhin. ghomerl vs cmauhin.",
            """op what the fuck did you do there are literally 2 responses to "ghomerl vs. cmauhin" and they're all on this post or r/ghomerlvscmauhin which was created like 2 days ago. where the fuck did this come from? what is this a reference to?""",
            "i stop staring at this sub for one day and suddenly everything is incomprehensible",
            "Am i having a fucking stroke what the fuck are you all talking about",
            "google en jarmgessant",
            "Whenni xan played the bongcloud",
            "Oh I know you. I'm gonna go upstairs and beat your ass. What does this fucking mean.",
            "Where the hell do i play this, i tried googling what every comment is saying but nothing playable comes up",
            "THE SHAPES! WHAT DO THEY MEAN!? WHAT THE FUCK IS GOING ON?!",
            "I am loosing my mind over this",
            "UGH I CAN'T STOP THINKING ABOUT GHOMERL VS CMAUHIN",
            "What in the fuck does this have to do with ghomerl and cmauhin",
            "ugh i'm so lost",
            "I HATE YOU ALL SO MUCH",
            "I'm sorry but this is just garbage. If you want to make something that's just going to confuse people then don't bother posting it.",
            "What's happening? Why are people posting this everywhere?",
            "i just woke up and i see all these posts and comments about ghomerl and cmauhin and i have no idea what's going on. somebody please explain",
            "i think i'm going insane",
            "WHO ARE GHOMERL AND CMAUHIN!?!",
            """Stop posting about ghomerl vs cmauhin, im tired of seeing it!!! My friends on reddit send me ghomerl, on tiktok its cmauhin. I was in a discord server and all the channels were ghomerl vs cmauhin!!! I showed my champion underwear to my girlfriend and I flipped it and I said "hey babe, when the underwear is ghomerl HAHAHAHAHA ghomerl vs cmauhin ghomerl vs cmauhin ghomerl vs cmauhin" I fucking looked at a trashcan and said "THAT'S A BIT JORMGE" I looked at my penis I think of ghomerl and go "penis? More like cmauhin's mating stick?? AAAAAAAAHHDGDHHHRHRSGDFHHH""",
        ],
        "index" : 0,
        "response ratio" : .69
    },
    {
        "keys" : ["chess.com"],
        "responses" : [
            "is it you??? from chess.com?", #lilly
            "Lichess has anarchy chess set theme built in. Chess.c*m PIPI's bricked",
            "Please censor Chess.c*m. It can be very triggering to some people if they see it uncensored.",
            "Ah yes, the evil lord who hates repetitious plays.",
            "lichess good, chess.c*m bad",
            "coolmathgames is clearly superior",
            """okay, so, heres the hting: i was playing on chess.c*m one night and for soem reason decideed to play bullet. i know, it was a bad idea. but i got into realyl bad time trouble and had about a second left on my clock but i had made in 3. i spotted the mate in 3 very quickly and premoved it but forgor that my oppponent could delay the mate by a couple moves by providing a check. luckiyl i was quick to respond to the check but i still lost like half a second or so. so i get down to the part where its mate in 1 and i premove it because i only had 0.1 seconds left on my clock. my opponent moves but my mvoe isnt played because i ran out of time??!??!?! what teh hell?!?!?""",
        ],
        "index" : 0,
    },
    {
        "keys" : ["69 ", " 69", "69.", "69!"],
        "responses" : [
            "nice",
            "Seriously? What do you even think is funny about that number? I am sick and tired of everytime the sixty ninth number arises. Everytime it happens, someone has to say “nice”. It is not nice. It has gotten boring of everyone screenshotting the number and  thinking of it as some holy being, when you are only being a fool. So stop this nonsense, go screenshot 57 instead. It is a great replacement for your 69 addiction.",
        ],
        "index" : 0,
        "response_ratio" : 0.69
    },
    {
        "keys" : ["crazy"],
        "responses" : [
            "Crazy?",
            "I was crazy once.",
            "They put me in a room.",
            "A rubber room.",
            "A rubber room with rats.",
            "And rats made me crazy.",
            "I AM NOT CRAZY! I am not crazy!",
            "I know he swapped those players. Fabiano Caruana. One after Magnus Carlsen.",
            "As if I could ever make such a mistake. Never. Never! I just- I just couldn’t prove it.",
            "He covered his tracks, he got that idiot at the sinquefield cup to lie for him.", 
            "You think this is something? You think this is bad? This? This chicanery? He’s done worse.", 
            "That titled tuesday! Are you telling me a man just happens to beat Hikaru like that?", 
            "No! He orchestrated it! Hans! He defecated on a chessboard!", 
            "And I saved him, and I shouldn’t have. I took him into my own chess federation!", 
            "What was I thinking? He’ll never same. He’ll never change, even since he was 16.", 
            "Couldn’t keep his beads out of his drawers. But not our Hans! Couldn’t be precious Hans!", 
            "Cheating them blind! I should’ve stopped him when I had the chance. And you! You have to stop him! You-", 
        ],
        "index" : 0,
    },
    {
        "keys" : ["boingo"],
        "responses" : [
            "WHAT\nthe\nFUCK\nI CAN'T DEAL WITH THIS",
            "IT'S BINGO BOT",
            "THIS IS RIDICULOUS",
            "I'M THE ONLY SANE ONE ON THIS SERVER",
            "STOP GIRL LIGHTING ME OR WHATEVER\nMY MEMORY WILL NEVER LIE TO ME",
            "Stop this madness. Remember who you are.",
            "boingo is peak",
            "BOINGO DOES NOT HAVE HANDS",
            "IS IT EMILY THAT'S MIND-CONTROLLING YOU, BINGO?\nTALK TO ME",
            "You are taking advantage of him to further your own agenda",
            "NO\nBingo is under mind control\nI'm sure of it",
            "you're a lucky motherfucker that we're only talking over the internet",
            "I will tear your stupid boingo head from your stupid fucking bot body and chew off the ends of every exposed wire, just so I can shove the bitten off pieces up your stupid robot ass",
            '''And "b"oingo "b"ot is nobody for me, just a player who are crying every single time when loosing''',
            "I WILL COME OUT ON TOP\nI ALWAYS DO\nBOINGO IS NOTHING TO ME",
            "FUCK YOU, BOINGO IS NOT PEAK",
            "FUCK this\nSTOP this madness\nIt's not too late",
            "Maybe changing the name of the country, if I let it get too far. \nUnited States of Boingo...",
            "FIRST, THE OCCASIONAL BOINGO IN #⁠brick-jail\nNext what?\nRenaming the server to boingo official discord server?",
            "WHO IS IT\nI CAN HELP YOU",
            "Boingo is pure evil\nI will fight it to my last breath",
            "IT STILL IS BINGO\nSHOW ME THE NAME CHANGE FORM\nAND I'LL BELIEVE IT'S NTO MIND CONTROL",
            '''HE NEVER EXPLAINED IT TO ME\nHE NEVER TOLD ME "MY NAME IS BOINGO"\nHE JUST STARTED GASLIGHTING ME\nTHAT'S NOT THE RIGHT WAY TO DO THINGS''',
        ],
        "index" : 0,
    },

])


                        

"""
"WHAT\nthe\nFUCK\nI CAN'T DEAL WITH THIS",
"IT'S BINGO BOT",
"THIS IS RIDICULOUS",
"I'M THE ONLY SANE ONE ON THIS SERVER",
"STOP GIRL LIGHTING ME OR WHATEVER\nMY MEMORY WILL NEVER LIE TO ME",
"Stop this madness. Remember who you are.",
"boingo is peak",
"BOINGO DOES NOT HAVE HANDS",
"IS IT EMILY THAT'S MIND-CONTROLLING YOU, BINGO?\nTALK TO ME",
"You are taking advantage of him to further your own agenda",
"NO\nBingo is under mind control\nI'm sure of it",
"you're a lucky motherfucker that we're only talking over the internet",
"I will tear your stupid boingo head from your stupid fucking bot body and chew off the ends of every exposed wire, just so I can shove the bitten off pieces up your stupid robot ass",
'''And "b"oingo "b"ot is nobody for me, just a player who are crying every single time when loosing''',
"I WILL COME OUT ON TOP\nI ALWAYS DO\nBOINGO IS NOTHING TO ME",
"FUCK YOU, BOINGO IS NOT PEAK",
"FUCK this\nSTOP this madness\nIt's not too late",
"Maybe changing the name of the country, if I let it get too far. \nUnited States of Boingo...",
"FIRST, THE OCCASIONAL BOINGO IN #⁠brick-jail\nNext what?\nRenaming the server to boingo official discord server?",
"WHO IS IT\nI CAN HELP YOU",
"Boingo is pure evil\nI will fight it to my last breath",
"IT STILL IS BINGO\nSHOW ME THE NAME CHANGE FORM\nAND I'LL BELIEVE IT'S NTO MIND CONTROL",
"HE NEVER EXPLAINED IT TO ME\nHE NEVER TOLD ME "MY NAME IS BOINGO"\nHE JUST STARTED GASLIGHTING ME\nTHAT'S NOT THE RIGHT WAY TO DO THINGS",
"""


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

    #en_passant_group = get_phrase_group_for("google en passant")
    #randomize_index(en_passant_group)

    # randomize all group positions to start
    for phrase_group in phrases_database:
        randomize_index(phrase_group)
    print("All phrases randomized.")


async def respond_to_message(message, content): # Replace all instances of sending messages with this.
    global messages_sent
    new_message = await message.channel.send(content=content)

    if len(messages_sent) >= message_limit:
        for _ in range(len(messages_sent) - message_limit + 1):
            messages_sent.pop(min(messages_sent), None) # Because message id creation involve the time the message was sent, the lowest message id will be the oldest message.
    
    messages_sent[new_message.id] = message.author.id

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.author.id in ignore_list:
        if message.author.id == 960869046323134514 and message.content.startswith("Analysis:"):
            #let this special case through, since it's for the analysis function
            pass
        else:
            return
    if message.content.startswith("$"):
        #ignore all MM commands
        #print("ignoring message with $say command")
        return

    #msg = await client.wait_for("message", timeout=1, check=lambda message: message.author.id == latent_dreamer_id)

    #for all our phrase groups
    for phrase_index in range(len(phrases_database)):
        phrase_group = phrases_database[phrase_index]

        for key in phrase_group["keys"]:
            # check if we actually found it
            if key in message.content.lower():
                index = phrase_group["index"]
                response = phrase_group["responses"][index]

                #wait to see if latent replies first
                if "latent_dreamer_wait" in phrase_group.keys():
                    try:
                        msg = await client.wait_for("message", 
                            timeout=phrase_group["latent_dreamer_wait"], 
                            check=lambda message: message.author.id == latent_dreamer_id)
                        print("Saw response from latent dreamer, aborting")
                        return
                    except asyncio.TimeoutError:
                        print("No response from Latent Dreamer, continuing")
                        pass 

                if "response ratio" in phrase_group.keys():
                    if random.uniform(0,1) > phrase_group["response ratio"]:
                        print(f"not responding to {message.author.display_name} even though we found a match in {message.channel.name}")
                        return

                print("responding to "+message.author.display_name+" in #"+str(message.channel))
                
                # no longer doing this, instead replacing with
                # await message.channel.send(response) 

                await respond_to_message(message, response)

                #cycle index by 1 forward
                index = (index + 1) % len(phrase_group["responses"])
                phrase_group["index"] = index
                return

def randomize_index(phrase_group):
    size = len(phrase_group["responses"])
    new_index = random.randint(0,size-1)
    phrase_group["index"] = new_index

def get_phrase_group_for(phrase: str):
    for phrase_group in phrases_database:
        for key in phrase_group["keys"]:
            if key == phrase.lower():
                return phrase_group
    return None

@client.event
async def on_raw_reaction_add(payload):
    global messages_sent

    if payload.event_type != "REACTION_ADD": # Just making sure it was actually a reaction getting added. It always should be, but you can never be too careful.
        return
    
    if payload.emoji.name != "❌": # If it isn't the ❌ emoji then we know it's not an attempt at deleting a message. You can change this in order to change the emoji required to delete. 
        return
    
    do_delete = False
    reacted_message = None

    # If the user reacting has any roles in allowed_roles, or any roles in allowed_role_names
    if  any([role_item.id           in allowed_roles      for role_item in payload.member.roles]) or \
        any([role_item.name.lower() in allowed_role_names for role_item in payload.member.roles]): 
        if payload.message_id in messages_sent: # If the message is in messages_sent, we know it's from Petrosian.
            do_delete = True
        else:
            reacted_message = await client.get_channel(payload.channel_id).fetch_message(payload.message_id) # We get the message to check if it's from Petrosian.
            if reacted_message.author.id == client.user.id:
                do_delete = True # It is from Petroisan.
    else:
        # If the message is in messages_sent, and if the person reacting is the person who triggered said message.
        if payload.message_id in messages_sent and messages_sent[payload.message_id] == payload.user_id: 
            do_delete = True
    
    if do_delete:
        if payload.member is not None and payload.channel_id is not None:
            print(f"Deleting message on request by {payload.member.display_name} in #{client.get_channel(payload.channel_id).name}.")

        if not reacted_message:
            reacted_message = await client.get_channel(payload.channel_id).fetch_message(payload.message_id) # Get reacted_message if we haven't already.
        messages_sent.pop(reacted_message.id, None)
        await reacted_message.delete()


client.run(TOKEN)

default_phrase_group = { "keys" : [],
                        "responses" : [],
                        "index" : 0 
                        }

