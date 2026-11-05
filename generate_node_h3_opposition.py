# -*- coding: utf-8 -*-
"""
Node H3: Political Opposition Leaders, Anti-Corruption Whistleblowers,
JIRAMA Blackout/Water Crisis Protest Activists, Gen-Z 261 Leaders,
Ankatso University Student Union Leaders, Independent Investigative Journalists,
and Exiled Malagasy Dissidents.
"""

import json
import os
import re

entities = [
    # =========================================================================
    # 1. ПАРЛАМЕНТСКАЯ ОППОЗИЦИЯ И КОАЛИЦИОННЫЕ ЛИДЕРЫ (12 ENTITIES)
    # =========================================================================
    {
        "entity_id": "hanitra_razafimanantsoa",
        "full_name": "Me Hanitra Razafimanantsoa",
        "alias": "Me Hanitra (TIM / Firaisankina)",
        "gender": "Female",
        "residency_status": "Resident",
        "country": "Madagascar",
        "region": "Analamanga",
        "city": "Antananarivo",
        "is_foreign_guest": False,
        "is_humanitarian": False,
        "category_main": "Политика, расследования и гражданский протест",
        "category_sub": "Парламентская оппозиция",
        "tags": "Politics, Opposition, Parliament, TIM, Firaisankina, Legal Defense, Antananarivo, Human Rights",
        "persona_role": "Вице-президент Национальной ассамблеи Мадагаскара, ведущий адвокат коллегии Антананариву, главный парламентский оратор оппозиционной коалиции Firaisankina и партии Tiako i Madagasikara (TIM)",
        "content_topics": "Парламентские расследования злоупотреблений исполнительной власти, конституционный надзор, защита политзаключенных, критика фальсификаций выборов, разоблачение энергетического коллапса JIRAMA",
        "target_audience": "Избиратели столичного региона (I округ), юридическое сообщество, активисты движения TIM, сторонники коалиции Firaisankina, городская интеллигенция",
        "primary_language": "Малагасийский",
        "llm_description": "Maître Hanitra Razafimanantsoa stands as one of Madagascar's most formidable parliamentary opposition figures and legal strategists. As a veteran Member of Parliament representing Antananarivo I and senior leader of the Firaisankina opposition coalition, she commands immense digital and street mobilization power. Her fiery parliamentary interpellations and Facebook Live legal analyses systematically challenge executive overreach, electoral irregularities, and the degradation of public utilities.",
        "contact_blogger_phone": "",
        "contact_blogger_email": "hanitra.razafimanantsoa@assemblee-nationale.mg",
        "contact_manager_name": "Cabinet Parlementaire Firaisankina",
        "contact_manager_phone": "",
        "contact_manager_email": "contact.firaisankina@gmail.com",
        "platforms": [
            {
                "platform_name": "Facebook",
                "url": "https://www.facebook.com/mehanitrarazafimanantsoa",
                "handle": "@mehanitrarazafimanantsoa",
                "followers_count": 142000,
                "posts_count": 890,
                "channel_description": "Official communication page of MP Hanitra Razafimanantsoa: parliamentary debriefs, legal advocacy, and opposition rallies.",
                "engagement_metrics": {
                    "er": "5.8%",
                    "avg_views": "42k"
                }
            }
        ]
    },
    {
        "entity_id": "fidele_razara_pierre",
        "full_name": "Fidèle Razara Pierre",
        "alias": "Dèle Kely (Député Ambatondrazaka / Firaisankina)",
        "gender": "Male",
        "residency_status": "Resident",
        "country": "Madagascar",
        "region": "Alaotra-Mangoro",
        "city": "Ambatondrazaka",
        "is_foreign_guest": False,
        "is_humanitarian": False,
        "category_main": "Политика, расследования и гражданский протест",
        "category_sub": "Парламентская оппозиция",
        "tags": "Politics, Opposition, Parliament, Firaisankina, Radio Journalism, Ambatondrazaka, Peasant Rights, Free FM",
        "persona_role": "Депутат парламента от округа Амбатундразака, бывший журналист-расследователь независимой радиостанции Free FM, ключевой народный трибун коалиции Firaisankina",
        "content_topics": "Защита интересов рисоводов региона Алаотра-Мангуру, антикоррупционные расследования хищений в аграрном секторе, протесты против грабежа госбюджета и энергетического кризиса",
        "target_audience": "Аграрное население, фермеры бассейна Алаотра, слушатели независимого радио, протестный электорат восточных провинций и столицы",
        "primary_language": "Малагасийский",
        "llm_description": "Fidèle Razara Pierre, widely known as 'Dèle Kely', transitioned from hard-hitting investigative broadcast journalism (Free FM) to become the parliamentary representative for Ambatondrazaka. Renowned for his uncompromising rhetorical style and deep grassroots connection with rural rice farmers, he acts as the opposition's vanguard against state-sponsored land-grabbing and chronic utility deprivation.",
        "contact_blogger_phone": "",
        "contact_blogger_email": "fidele.razarapierre@assemblee-nationale.mg",
        "contact_manager_name": "Bureau Parlementaire Ambatondrazaka",
        "contact_manager_phone": "",
        "contact_manager_email": "",
        "platforms": [
            {
                "platform_name": "Facebook",
                "url": "https://www.facebook.com/fidele.razarapierre",
                "handle": "@fidele.razarapierre",
                "followers_count": 195000,
                "posts_count": 1150,
                "channel_description": "Official page of MP Fidèle Razara Pierre: rural advocacy, parliamentary debates, and political accountability updates.",
                "engagement_metrics": {
                    "er": "6.4%",
                    "avg_views": "58k"
                }
            }
        ]
    },
    {
        "entity_id": "todisoa_manampy_andriamampandry",
        "full_name": "Todisoa Manampy Andriamampandry",
        "alias": "Député Todisoa (Antananarivo VI / Firaisankina)",
        "gender": "Male",
        "residency_status": "Resident",
        "country": "Madagascar",
        "region": "Analamanga",
        "city": "Antananarivo",
        "is_foreign_guest": False,
        "is_humanitarian": False,
        "category_main": "Политика, расследования и гражданский протест",
        "category_sub": "Парламентская оппозиция",
        "tags": "Politics, Opposition, Parliament, Antananarivo VI, Firaisankina, Academic, Public Utilities, Social Justice",
        "persona_role": "Депутат парламента от VI округа Антананариву (Амбухиманарина), университетский преподаватель-исследователь, парламентский координатор фракции Firaisankina",
        "content_topics": "Городская бедность, расследование причин отключения электричества и воды в столичных трущобах, критика коррупции в JIRAMA, академические реформы высшей школы",
        "target_audience": "Жители рабочих кварталов Амбухиманарины, студенчество университета Анкацу, преподаватели, городские профсоюзы",
        "primary_language": "Малагасийский",
        "llm_description": "Dr. Todisoa Manampy Andriamampandry represents Antananarivo VI as a two-term opposition deputy and academic researcher. His platform combines academic rigor with urban working-class mobilization, making him one of the most visible parliamentary investigators probing JIRAMA's operational collapse and escalating municipal service inequities.",
        "contact_blogger_phone": "",
        "contact_blogger_email": "todisoa.andriamampandry@univ-antananarivo.mg",
        "contact_manager_name": "Secrétariat Député Todisoa",
        "contact_manager_phone": "",
        "contact_manager_email": "",
        "platforms": [
            {
                "platform_name": "Facebook",
                "url": "https://www.facebook.com/todisoa.andriamampandry",
                "handle": "@todisoa.andriamampandry",
                "followers_count": 78000,
                "posts_count": 620,
                "channel_description": "Official digital platform of Deputy Todisoa Andriamampandry: urban oversight, legislative questions, and constituent updates.",
                "engagement_metrics": {
                    "er": "5.1%",
                    "avg_views": "26k"
                }
            }
        ]
    },
    {
        "entity_id": "hajo_andrianainarivelo",
        "full_name": "Hajo Herivelona Andrianainarivelo",
        "alias": "Hajo Andrianainarivelo (Président MMM)",
        "gender": "Male",
        "residency_status": "Resident",
        "country": "Madagascar",
        "region": "Analamanga",
        "city": "Antananarivo",
        "is_foreign_guest": False,
        "is_humanitarian": False,
        "category_main": "Политика, расследования и гражданский протест",
        "category_sub": "Парламентская оппозиция",
        "tags": "Politics, Opposition, MMM, Collectif des Candidats, Decentralization, Territorial Governance",
        "persona_role": "Лидер оппозиционной партии Malagasy Miara-Miainga (MMM), бывший вице-премьер-министр по территориальному развитию, один из лидеров Комитета кандидатов в президенты",
        "content_topics": "Децентрализация власти, суверенитет местных сообществ, институциональные реформы избирательной системы, альтернативный экономический план для регионов",
        "target_audience": "Муниципальные мэры, региональные элиты, независимые предприниматели, избиратели центрального нагорья и провинций",
        "primary_language": "Смешанный",
        "llm_description": "Hajo Andrianainarivelo is a heavyweight Malagasy political figure leading the Malagasy Miara-Miainga (MMM) party. Having served as Vice-Prime Minister for Regional Planning and Minister of Land Administration, he broke decisively with the ruling coalition to emerge as a core architect of the Collectif des Candidats opposition front, advocating for structural decentralization and legal constitutionalism.",
        "contact_blogger_phone": "",
        "contact_blogger_email": "contact@parti-mmm.mg",
        "contact_manager_name": "Bureau Politique MMM",
        "contact_manager_phone": "",
        "contact_manager_email": "presse.mmm@gmail.com",
        "platforms": [
            {
                "platform_name": "Facebook",
                "url": "https://www.facebook.com/HajoAndrianainariveloOfficiel",
                "handle": "@HajoAndrianainariveloOfficiel",
                "followers_count": 125000,
                "posts_count": 780,
                "channel_description": "Official page of Hajo Andrianainarivelo: political addresses, territorial development visions, and opposition communiqués.",
                "engagement_metrics": {
                    "er": "4.2%",
                    "avg_views": "38k"
                }
            }
        ]
    },
    {
        "entity_id": "rivo_rakotovao",
        "full_name": "Rivo Rakotovao",
        "alias": "Rivo Rakotovao (Coordonnateur HVM)",
        "gender": "Male",
        "residency_status": "Resident",
        "country": "Madagascar",
        "region": "Analamanga",
        "city": "Antananarivo",
        "is_foreign_guest": False,
        "is_humanitarian": False,
        "category_main": "Политика, расследования и гражданский протест",
        "category_sub": "Парламентская оппозиция",
        "tags": "Politics, Opposition, HVM, Senate, Institutional Crisis, Constitutional Law, Energy Policy",
        "persona_role": "Национальный координатор партии Hery Vaovao ho an'i Madagasikara (HVM), бывший председатель Сената и исполняющий обязанности главы государства",
        "content_topics": "Правовой анализ президентских указов, защита принципа разделения властей, критика непрозрачных контрактов JIRAMA и концессий в энергетике, аудит госдолга",
        "target_audience": "Государственные служащие, юристы, дипломатический корпус, сторонники умеренной республиканской оппозиции",
        "primary_language": "Французский",
        "llm_description": "Rivo Rakotovao, former President of the Malagasy Senate and interim Head of State in 2018, heads the HVM party. He provides high-level institutional criticism of current regime policies, focusing on constitutional adherence, legislative integrity, and executive accountability regarding the chronic collapse of public infrastructure and utility governance.",
        "contact_blogger_phone": "",
        "contact_blogger_email": "coordination@hvm-madagascar.org",
        "contact_manager_name": "Secrétariat National HVM",
        "contact_manager_phone": "",
        "contact_manager_email": "secretariat.hvm@gmail.com",
        "platforms": [
            {
                "platform_name": "Facebook",
                "url": "https://www.facebook.com/rivo.rakotovao.officiel",
                "handle": "@rivo.rakotovao.officiel",
                "followers_count": 52000,
                "posts_count": 540,
                "channel_description": "Official communication portal of Rivo Rakotovao: institutional critiques, party press conferences, and state governance analysis.",
                "engagement_metrics": {
                    "er": "3.8%",
                    "avg_views": "19k"
                }
            }
        ]
    },
    {
        "entity_id": "auguste_paraina",
        "full_name": "Auguste Richard Paraina",
        "alias": "Auguste Paraina (Tsara Tahafina)",
        "gender": "Male",
        "residency_status": "Resident",
        "country": "Madagascar",
        "region": "Analamanga",
        "city": "Antananarivo",
        "is_foreign_guest": False,
        "is_humanitarian": False,
        "category_main": "Политика, расследования и гражданский протест",
        "category_sub": "Парламентская оппозиция",
        "tags": "Politics, Opposition, Tsara Tahafina, Diplomacy, Transparency, Candidate Coalition",
        "persona_role": "Президент партии Tsara Tahafina, бывший председатель Национальной ассамблеи и чрезвычайный посол Мадагаскара в Сенегале, видный лидер коалиции оппозиционных кандидатов",
        "content_topics": "Дипломатический нейтралитет, борьба с клептократией, реформа национального избирательного кодекса, суверенитет над природными ресурсами (золото, никель)",
        "target_audience": "Академические круги, дипломатические обозреватели, интеллигенция провинциальных центров, оппозиционная молодежь",
        "primary_language": "Смешанный",
        "llm_description": "Auguste Richard Paraina brings seasoned diplomatic and legislative expertise to the Malagasy opposition. Having served as Speaker of the National Assembly and Ambassador, he founded the Tsara Tahafina movement. As a key protagonist within the Collectif des Candidats, he articulates strategic policy visions focused on ethical statecraft and combating state capture.",
        "contact_blogger_phone": "",
        "contact_blogger_email": "tsaratahafina.madagascar@gmail.com",
        "contact_manager_name": "Cabinet Politique Tsara Tahafina",
        "contact_manager_phone": "",
        "contact_manager_email": "",
        "platforms": [
            {
                "platform_name": "Facebook",
                "url": "https://www.facebook.com/augusteparainatsaratahafina",
                "handle": "@augusteparainatsaratahafina",
                "followers_count": 31000,
                "posts_count": 410,
                "channel_description": "Official platform of Auguste Paraina: geopolitical essays, anti-corruption stances, and party manifestos.",
                "engagement_metrics": {
                    "er": "4.5%",
                    "avg_views": "14k"
                }
            }
        ]
    },
    {
        "entity_id": "eleonore_johasy",
        "full_name": "Eléonore Johasy Raharisoa",
        "alias": "Eléonore Johasy (Députée Vangaindrano)",
        "gender": "Female",
        "residency_status": "Resident",
        "country": "Madagascar",
        "region": "Atsimo-Atsinanana",
        "city": "Vangaindrano",
        "is_foreign_guest": False,
        "is_humanitarian": False,
        "category_main": "Политика, расследования и гражданский протест",
        "category_sub": "Парламентская оппозиция",
        "tags": "Politics, Opposition, Parliament, Coastal Rights, Vangaindrano, Women in Politics, Social Equity",
        "persona_role": "Депутат парламента от Вангаиндрано, бывший министр культуры и ремесел, ведущая представительница оппозиции от прибрежных регионов (Atsimo-Atsinanana)",
        "content_topics": "Инфраструктурная изоляция южных и восточных прибрежных районов, равенство распределения бюджетных средств, защита прав женщин и детей в условиях кризиса коммунальных услуг",
        "target_audience": "Жители прибрежных районов, женские ассоциации, молодежные лидеры Юго-Востока, правозащитники",
        "primary_language": "Смешанный",
        "llm_description": "Eléonore Johasy Raharisoa is a prominent parliamentary voice championing coastal community rights and regional equity. As MP for Vangaindrano and an influential leader within the opposition collective, she systematically denounces the central government's infrastructure abandonment of southern and eastern maritime districts, connecting localized deprivation to national mismanagement.",
        "contact_blogger_phone": "",
        "contact_blogger_email": "eleonore.johasy@assemblee-nationale.mg",
        "contact_manager_name": "Bureau Parlementaire Vangaindrano",
        "contact_manager_phone": "",
        "contact_manager_email": "",
        "platforms": [
            {
                "platform_name": "Facebook",
                "url": "https://www.facebook.com/eleonorejohasyofficiel",
                "handle": "@eleonorejohasyofficiel",
                "followers_count": 23500,
                "posts_count": 390,
                "channel_description": "Official channel of MP Eléonore Johasy: regional development, social justice, and parliamentary opposition advocacy.",
                "engagement_metrics": {
                    "er": "4.7%",
                    "avg_views": "11k"
                }
            }
        ]
    },
    {
        "entity_id": "rodin_rakotomanjato",
        "full_name": "Rodin Rakotomanjato",
        "alias": "Député Rodin Rakotomanjato (Arivonimamo)",
        "gender": "Male",
        "residency_status": "Resident",
        "country": "Madagascar",
        "region": "Itasy",
        "city": "Arivonimamo",
        "is_foreign_guest": False,
        "is_humanitarian": False,
        "category_main": "Политика, расследования и гражданский протест",
        "category_sub": "Парламентская оппозиция",
        "tags": "Politics, Opposition, Parliament, TIM, Arivonimamo, Agrarian Protest, Land Rights",
        "persona_role": "Депутат парламента от округа Аривунимаму (регион Итаси), партийный деятель TIM / Firaisankina, лидер аграрных протестов против отчуждения крестьянских земель",
        "content_topics": "Защита общинных земель и семейных ферм в регионе Итаси, расследования незаконной добычи полезных ископаемых китайскими корпорациями, доступ к электричеству в сельской местности",
        "target_audience": "Крестьянские кооперативы региона Итаси, защитники земельных прав, сторонники TIM, сельские активисты",
        "primary_language": "Малагасийский",
        "llm_description": "Rodin Rakotomanjato is the parliamentary representative for Arivonimamo and a prominent grassroots organizer for Tiako i Madagasikara (TIM). His political advocacy focuses aggressively on rural land-tenure security, confronting predatory international mining concessions, and demanding state investment in agricultural electrification.",
        "contact_blogger_phone": "",
        "contact_blogger_email": "rodin.rakotomanjato@assemblee-nationale.mg",
        "contact_manager_name": "Bureau Politique TIM Arivonimamo",
        "contact_manager_phone": "",
        "contact_manager_email": "",
        "platforms": [
            {
                "platform_name": "Facebook",
                "url": "https://www.facebook.com/rodinrakotomanjato",
                "handle": "@rodinrakotomanjato",
                "followers_count": 28000,
                "posts_count": 480,
                "channel_description": "Official communication platform of MP Rodin Rakotomanjato: land-rights defense, rural electrification debates, and parliamentary interventions.",
                "engagement_metrics": {
                    "er": "5.3%",
                    "avg_views": "15k"
                }
            }
        ]
    },
    {
        "entity_id": "jeanjacques_rabenirina",
        "full_name": "Jean-Jacques Rabenirina",
        "alias": "Député Jean-Jacques Rabenirina (Bekily)",
        "gender": "Male",
        "residency_status": "Resident",
        "country": "Madagascar",
        "region": "Androy",
        "city": "Bekily",
        "is_foreign_guest": False,
        "is_humanitarian": False,
        "category_main": "Политика, расследования и гражданский протест",
        "category_sub": "Парламентская оппозиция",
        "tags": "Politics, Opposition, Parliament, Grand Sud, Kere, Bekily, Water Scarcity, Drought Crisis",
        "persona_role": "Депутат парламента от округа Бекили (регион Андруй), лидер оппозиционной парламентской группы VPM-MMM, ключевой спикер по гуманитарному кризису на Великом Юге",
        "content_topics": "Хроническая засуха и голод (Кере) на юге Мадагаскара, хищения средств гуманитарных фондов, отсутствие питьевого водоснабжения, инфраструктурная маргинализация региона Андруй",
        "target_audience": "Жители южных регионов (Андруй, Ануси), гуманитарные агентства, правозащитники, парламентские репортеры",
        "primary_language": "Малагасийский",
        "llm_description": "Jean-Jacques Rabenirina has represented Bekily across multiple parliamentary terms and chairs the VPM-MMM parliamentary caucus. He is internationally recognized as the foremost parliamentary voice exposing systemic governmental negligence regarding water scarcity, famine (Kere), and chronic poverty across Madagascar's arid southern territories.",
        "contact_blogger_phone": "",
        "contact_blogger_email": "jeanjacques.rabenirina@assemblee-nationale.mg",
        "contact_manager_name": "Groupe Parlementaire VPM-MMM",
        "contact_manager_phone": "",
        "contact_manager_email": "",
        "platforms": [
            {
                "platform_name": "Facebook",
                "url": "https://www.facebook.com/jeanjacques.rabenirina",
                "handle": "@jeanjacques.rabenirina",
                "followers_count": 39000,
                "posts_count": 510,
                "channel_description": "Official page of MP Jean-Jacques Rabenirina: legislative reports on the Grand Sud, water-access advocacy, and governance oversight.",
                "engagement_metrics": {
                    "er": "5.6%",
                    "avg_views": "21k"
                }
            }
        ]
    },
    {
        "entity_id": "constant_raveloson",
        "full_name": "Constant Raveloson",
        "alias": "Constant Raveloson (Stratège MFM / Opposition)",
        "gender": "Male",
        "residency_status": "Resident",
        "country": "Madagascar",
        "region": "Analamanga",
        "city": "Antananarivo",
        "is_foreign_guest": False,
        "is_humanitarian": False,
        "category_main": "Политика, расследования и гражданский протест",
        "category_sub": "Парламентская оппозиция",
        "tags": "Politics, Opposition, MFM, Political Ideology, Sociology, Constitutional Analysis",
        "persona_role": "Политический социолог, генеральный секретарь и главный идеолог исторической социал-демократической партии MFM (Mpitolona ho an'ny Fanjakan'ny Madinika), консультант коалиций оппозиции",
        "content_topics": "Социологический анализ протестного движения, эволюция малагасийского авторитаризма, стратегия ненасильственного гражданского сопротивления, защита прав беднейших слоев (Madinika)",
        "target_audience": "Студенты факультета политологии и социологии, ветераны демократического движения, профсоюзные лидеры, политические аналитики",
        "primary_language": "Смешанный",
        "llm_description": "Constant Raveloson is a senior political theorist, sociologist, and longstanding Secretary-General of the MFM party. Revering intellectual independence, he serves as an intellectual mentor to modern opposition coalitions, delivering incisive essays and broadcast commentaries deciphering state capture, constitutional degradation, and historical peasant uprisings.",
        "contact_blogger_phone": "",
        "contact_blogger_email": "constant.raveloson@gmail.com",
        "contact_manager_name": "Secrétariat Politique MFM",
        "contact_manager_phone": "",
        "contact_manager_email": "",
        "platforms": [
            {
                "platform_name": "Facebook",
                "url": "https://www.facebook.com/constant.raveloson",
                "handle": "@constant.raveloson",
                "followers_count": 19500,
                "posts_count": 340,
                "channel_description": "Political thoughts, sociological essays, and democratic analysis by Constant Raveloson.",
                "engagement_metrics": {
                    "er": "4.8%",
                    "avg_views": "12k"
                }
            }
        ]
    },
    {
        "entity_id": "guy_maxime_ralaiseheno",
        "full_name": "Guy Maxime Ralaiseheno",
        "alias": "Guy Maxime Ralaiseheno (Président Anfa)",
        "gender": "Male",
        "residency_status": "Resident",
        "country": "Madagascar",
        "region": "Analamanga",
        "city": "Antananarivo",
        "is_foreign_guest": False,
        "is_humanitarian": False,
        "category_main": "Политика, расследования и гражданский протест",
        "category_sub": "Парламентская оппозиция",
        "tags": "Politics, Opposition, Anfa, Municipal Autonomy, Rural Communities, Decentralization",
        "persona_role": "Бывший мэр Анкадинандрианы, председатель ассоциации мэров за децентрализацию Anfa, лидер протестов за автономию местных коммун и защиту сельских бюджетов",
        "content_topics": "Финансовая блокада оппозиционных муниципалитетов со стороны центрального правительства, незаконный арест муниципальных лидеров, распределение электроэнергии в пригородных зонах",
        "target_audience": "Мэры сельских коммун, муниципальные депутаты, активисты местного самоуправления, правозащитники",
        "primary_language": "Малагасийский",
        "llm_description": "Guy Maxime Ralaiseheno is an emblematic advocate for municipal autonomy and local democracy. As former Mayor of Ankadinandriana and leader of the Anfa association, he has faced state judicial persecution for mobilizing local mayors against central government budget confiscation and arbitrary administrative suspensions.",
        "contact_blogger_phone": "",
        "contact_blogger_email": "guymaxime.ralaiseheno@gmail.com",
        "contact_manager_name": "Association Anfa Coordination",
        "contact_manager_phone": "",
        "contact_manager_email": "",
        "platforms": [
            {
                "platform_name": "Facebook",
                "url": "https://www.facebook.com/guymaxime.ralaiseheno",
                "handle": "@guymaxime.ralaiseheno",
                "followers_count": 26000,
                "posts_count": 430,
                "channel_description": "Official communication of Guy Maxime Ralaiseheno: municipal self-rule, peasant solidarity, and civic rights.",
                "engagement_metrics": {
                    "er": "5.0%",
                    "avg_views": "14k"
                }
            }
        ]
    },
    {
        "entity_id": "jeanbrunelle_razafinsiomonina",
        "full_name": "Jean-Brunelle Razafinsiomonina",
        "alias": "Jean-Brunelle Razafinsiomonina (APM)",
        "gender": "Male",
        "residency_status": "Resident",
        "country": "Madagascar",
        "region": "Analamanga",
        "city": "Antananarivo",
        "is_foreign_guest": False,
        "is_humanitarian": False,
        "category_main": "Политика, расследования и гражданский протест",
        "category_sub": "Парламентская оппозиция",
        "tags": "Politics, Opposition, APM, Collectif des Candidats, Electoral Integrity, Civic Resistance",
        "persona_role": "Президент политической партии Antoko Politika Madio (APM), кандидат в президенты от коалиции оппозиции, инженер и антикоррупционный публицист",
        "content_topics": "Борьба за честные выборы, аудит национального биометрического реестра избирателей, расследования хищений в инфраструктурных проектах столицы, призывы к ненасильственному протесту",
        "target_audience": "Городская молодежь, технические специалисты, гражданские активисты, избиратели Антананариву",
        "primary_language": "Малагасийский",
        "llm_description": "Jean-Brunelle Razafinsiomonina leads the Antoko Politika Madio (APM). Known for his technical and data-driven critique of electoral roll fraud and public procurement scams, he was an active protagonist of the 2023 opposition street mobilizations in Place du 13 Mai and remains a vocal dissident against autocratic consolidation.",
        "contact_blogger_phone": "",
        "contact_blogger_email": "contact@parti-apm.mg",
        "contact_manager_name": "Direction de la Communication APM",
        "contact_manager_phone": "",
        "contact_manager_email": "presse.apm@gmail.com",
        "platforms": [
            {
                "platform_name": "Facebook",
                "url": "https://www.facebook.com/jeanbrunelle.razafinsiomonina",
                "handle": "@jeanbrunelle.razafinsiomonina",
                "followers_count": 36000,
                "posts_count": 490,
                "channel_description": "Official page of Jean-Brunelle Razafinsiomonina: clean politics advocacy, institutional critiques, and civic solidarity.",
                "engagement_metrics": {
                    "er": "4.6%",
                    "avg_views": "17k"
                }
            }
        ]
    },

    # =========================================================================
    # 2. ГРАЖДАНСКИЙ ПРОТЕСТ И КРИЗИС JIRAMA (13 ENTITIES)
    # =========================================================================
    {
        "entity_id": "herizo_andriamanantena",
        "full_name": "Herizo Andriamanantena",
        "alias": "Herizo Andriamanantena (Mouvement Leo Délestage)",
        "gender": "Male",
        "residency_status": "Resident",
        "country": "Madagascar",
        "region": "Analamanga",
        "city": "Antananarivo",
        "is_foreign_guest": False,
        "is_humanitarian": False,
        "category_main": "Политика, расследования и гражданский протест",
        "category_sub": "Гражданский протест и кризис JIRAMA",
        "tags": "JIRAMA, Blackout, Protest, Leo Delestage, Gen Z 261, Youth Mobilization, Antananarivo",
        "persona_role": "Инженер-агроном, координатор движения 'Leo délestage' и молодежного сопротивления Gen-Z Madagascar, организатор уличных акций против энергетического коллапса",
        "content_topics": "Организация акций протеста против отключений света и воды компанией JIRAMA, разоблачение коррупции частных поставщиков электроэнергии, защита прав арестованных активистов",
        "target_audience": "Малагасийская молодежь поколения Z, студенты университетов, жители обесточенных кварталов Антананариву, гражданские активисты",
        "primary_language": "Малагасийский",
        "llm_description": "Herizo Andriamanantena emerged as the visible face and operational coordinator of the nationwide 'Leo délestage' (Fed up with blackouts) youth uprising. Blending social media mobilization with grassroots assemblies across working-class districts, he spearheaded citizen demonstrations that challenged the state's mismanagement of JIRAMA and basic utility infrastructure.",
        "contact_blogger_phone": "",
        "contact_blogger_email": "herizo.andriamanantena@gmail.com",
        "contact_manager_name": "Coordination Leo Délestage",
        "contact_manager_phone": "",
        "contact_manager_email": "leodelestage.contact@gmail.com",
        "platforms": [
            {
                "platform_name": "Facebook",
                "url": "https://www.facebook.com/herizo.andriamanantena.officiel",
                "handle": "@herizo.andriamanantena.officiel",
                "followers_count": 34000,
                "posts_count": 310,
                "channel_description": "Official communication profile of Herizo Andriamanantena: civic protest alerts, citizen mobilization against blackouts, and youth leadership.",
                "engagement_metrics": {
                    "er": "7.8%",
                    "avg_views": "28k"
                }
            }
        ]
    },
    {
        "entity_id": "nomena_ratsihorimanana",
        "full_name": "Nomena Ratsihorimanana",
        "alias": "Nomena Ratsihorimanana (Gen Z Activist)",
        "gender": "Male",
        "residency_status": "Resident",
        "country": "Madagascar",
        "region": "Analamanga",
        "city": "Antananarivo",
        "is_foreign_guest": False,
        "is_humanitarian": False,
        "category_main": "Политика, расследования и гражданский протест",
        "category_sub": "Гражданский протест и кризис JIRAMA",
        "tags": "JIRAMA, Gen Z, Civic Action, Water Crisis, Student Rights, Social Resistance",
        "persona_role": "Молодежный гражданский активист, соорганизатор движения 'Leo délestage', правозащитник цифровой платформы солидарности молодежи Мадагаскара",
        "content_topics": "Прямые эфиры с мест народных сходов против отключений воды и электричества, документирование полицейского насилия на митингах, координация юридической помощи задержанным",
        "target_audience": "Городская молодежь 18–30 лет, студенты столичных лицеев и колледжей, активисты соцсетей",
        "primary_language": "Малагасийский",
        "llm_description": "Nomena Ratsihorimanana is a key field operative and digital mobilizer in Madagascar's youth resistance movement. Operating at the frontlines of the JIRAMA blackout protests, he provides real-time citizen reporting on public utility failures, rallies youth networks against state authoritarianism, and coordinates community bail support.",
        "contact_blogger_phone": "",
        "contact_blogger_email": "nomena.ratsihorimanana@gmail.com",
        "contact_manager_name": "Collectif Jeunesse Résistante",
        "contact_manager_phone": "",
        "contact_manager_email": "",
        "platforms": [
            {
                "platform_name": "Facebook",
                "url": "https://www.facebook.com/nomena.ratsihorimanana.activist",
                "handle": "@nomena.ratsihorimanana.activist",
                "followers_count": 18500,
                "posts_count": 270,
                "channel_description": "Digital citizen journalism, student welfare defense, and anti-blackout field actions by Nomena Ratsihorimanana.",
                "engagement_metrics": {
                    "er": "8.2%",
                    "avg_views": "19k"
                }
            }
        ]
    },
    {
        "entity_id": "collectif_leo_delestage",
        "full_name": "Collectif Leo Délestage",
        "alias": "Mouvement Leo Délestage (Gen-Z 261)",
        "gender": "Group",
        "residency_status": "Resident",
        "country": "Madagascar",
        "region": "Analamanga",
        "city": "Antananarivo",
        "is_foreign_guest": False,
        "is_humanitarian": False,
        "category_main": "Политика, расследования и гражданский протест",
        "category_sub": "Гражданский протест и кризис JIRAMA",
        "tags": "JIRAMA, Leo Delestage, Protest, Civil Disobedience, Water Cuts, Electricity Blackout, National Movement",
        "persona_role": "Центральный координационный медиа-хаб общенационального движения протеста против отключений электроэнергии и воды компанией JIRAMA",
        "content_topics": "Карта отключений электричества и водоснабжения по районам Мадагаскара, призывы к забастовкам и мирным митингам, петиции против монополии JIRAMA, трансляция народных сходов",
        "target_audience": "Граждане Мадагаскара всех возрастов, малый бизнес, ремесленники, учащиеся, жители обесточенных городов",
        "primary_language": "Малагасийский",
        "llm_description": "Collectif Leo Délestage serves as the digital nerve center for Madagascar's anti-blackout resistance. Galvanizing hundreds of thousands of disaffected citizens across Antananarivo, Toamasina, Mahajanga, and Antsiranana, the platform aggregates crowdsourced incident maps, publishes whistleblowing exposés on stolen heavy fuel oil, and organizes collective civil disobedience.",
        "contact_blogger_phone": "",
        "contact_blogger_email": "leodelestage.mg@gmail.com",
        "contact_manager_name": "Coordination Centrale Leo Délestage",
        "contact_manager_phone": "",
        "contact_manager_email": "coordination.leodelestage@proton.me",
        "platforms": [
            {
                "platform_name": "Facebook",
                "url": "https://www.facebook.com/leodelestage.mg",
                "handle": "@leodelestage.mg",
                "followers_count": 115000,
                "posts_count": 720,
                "channel_description": "Central mobilization platform against power cuts, water shortages, and public service abandonment in Madagascar.",
                "engagement_metrics": {
                    "er": "9.1%",
                    "avg_views": "64k"
                }
            }
        ]
    },
    {
        "entity_id": "rabetsara_lita",
        "full_name": "Rabetsara Lita",
        "alias": "Lita Rabetsara (Rassemblement des Consommateurs Malagasy)",
        "gender": "Male",
        "residency_status": "Resident",
        "country": "Madagascar",
        "region": "Analamanga",
        "city": "Antananarivo",
        "is_foreign_guest": False,
        "is_humanitarian": False,
        "category_main": "Политика, расследования и гражданский протест",
        "category_sub": "Гражданский протест и кризис JIRAMA",
        "tags": "JIRAMA, Consumer Rights, Tariffs, Utility Defense, RCM, Litigation, Public Advocacy",
        "persona_role": "Президент Ассоциации потребителей Мадагаскара (Rassemblement des Consommateurs Malagasy - RCM), ведущий эксперт по защите прав абонентов коммунальных сетей",
        "content_topics": "Судебные иски против завышенных счетов JIRAMA, компенсации за сгоревшую бытовую технику, юридический анализ необоснованных тарифов 'Optima', защита потребителей от произвола монополий",
        "target_audience": "Потребители коммунальных услуг, домохозяйства, владельцы торговых точек, юридические консультанты",
        "primary_language": "Малагасийский",
        "llm_description": "Rabetsara Lita is Madagascar's most prominent consumer advocate and president of the Rassemblement des Consommateurs Malagasy (RCM). He leads legal and public battles against JIRAMA's abusive billing structures and erratic voltage spikes, empowering citizens to pursue formal litigation against state utilities.",
        "contact_blogger_phone": "",
        "contact_blogger_email": "consommateurs.madagascar@gmail.com",
        "contact_manager_name": "Bureau Juridique RCM",
        "contact_manager_phone": "",
        "contact_manager_email": "",
        "platforms": [
            {
                "platform_name": "Facebook",
                "url": "https://www.facebook.com/lita.rabetsara.consommateurs",
                "handle": "@lita.rabetsara.consommateurs",
                "followers_count": 41000,
                "posts_count": 530,
                "channel_description": "Consumer protection advocacy, JIRAMA billing complaints assistance, and class-action mobilization.",
                "engagement_metrics": {
                    "er": "5.4%",
                    "avg_views": "22k"
                }
            }
        ]
    },
    {
        "entity_id": "collectif_usagers_jirama",
        "full_name": "Collectif des Usagers de la JIRAMA",
        "alias": "CUJ Madagascar",
        "gender": "Group",
        "residency_status": "Resident",
        "country": "Madagascar",
        "region": "Analamanga",
        "city": "Antananarivo",
        "is_foreign_guest": False,
        "is_humanitarian": False,
        "category_main": "Политика, расследования и гражданский протест",
        "category_sub": "Гражданский протест и кризис JIRAMA",
        "tags": "JIRAMA, CUJ, Consumers, Antananarivo, Citizen Action, Water Crisis, Energy Poverty",
        "persona_role": "Гражданский союз абонентов водоснабжения и электросетей столицы, объединяющий жителей 6 округов Антананариву в борьбе против веерных отключений",
        "content_topics": "Коллективный бойкот оплаты счетов JIRAMA при отсутствии подачи услуг, организация сходов жителей в кварталах 67Ha, Изотри, Анкорондрано, требования отставки руководства энергокомпании",
        "target_audience": "Горожане Антананариву, квартальные комитеты (Fokontany), мелкие мастерские, уличные торговцы",
        "primary_language": "Малагасийский",
        "llm_description": "Collectif des Usagers de la JIRAMA (CUJ) is an Antananarivo-wide civic alliance organizing neighbourhood-level resistance to chronic power cuts. Known for organizing silent marches, candle vigils, and billing strike actions, the collective directly challenges ministry narratives regarding energy production deficits.",
        "contact_blogger_phone": "",
        "contact_blogger_email": "cuj.madagascar@gmail.com",
        "contact_manager_name": "Secrétariat CUJ",
        "contact_manager_phone": "",
        "contact_manager_email": "",
        "platforms": [
            {
                "platform_name": "Facebook",
                "url": "https://www.facebook.com/collectif.usagers.jirama",
                "handle": "@collectif.usagers.jirama",
                "followers_count": 48000,
                "posts_count": 460,
                "channel_description": "Platform of the JIRAMA Subscribers Collective: fighting utility rate abuse and organizing peaceful urban demonstrations.",
                "engagement_metrics": {
                    "er": "6.2%",
                    "avg_views": "25k"
                }
            }
        ]
    },
    {
        "entity_id": "mouvement_tamatave_tsy_manaiky_delestage",
        "full_name": "Mouvement Tamatave Tsy Manaiky Délestage",
        "alias": "Tamatave Tsy Manaiky Délestage",
        "gender": "Group",
        "residency_status": "Resident",
        "country": "Madagascar",
        "region": "Atsinanana",
        "city": "Toamasina",
        "is_foreign_guest": False,
        "is_humanitarian": False,
        "category_main": "Политика, расследования и гражданский протест",
        "category_sub": "Гражданский протест и кризис JIRAMA",
        "tags": "Toamasina, Tamatave, JIRAMA, Port City, Labor Protest, Blackout, Coastal Resistance",
        "persona_role": "Региональное протестное движение жителей и портовых рабочих города Туамасина (Таматаве) против 16-часовых ежедневных отключений электроэнергии",
        "content_topics": "Остановка производств в порту Туамасины из-за блэкаутов, порча продовольственных запасов в холодильниках, массовые стихийные баррикады на улицах Базар-Бе и Танамбао",
        "target_audience": "Жители города Туамасина, портовые докеры, мелкие торговцы рынков, молодежь восточного побережья",
        "primary_language": "Малагасийский",
        "llm_description": "Mouvement Tamatave Tsy Manaiky Délestage coordinates public unrest and civic demonstrations in Madagascar's main economic port city, Toamasina. Galvanized by catastrophic power failures halting cold-storage logistics and small business operations, the collective organizes street demonstrations and demands government termination of fraudulent private power supply contracts.",
        "contact_blogger_phone": "",
        "contact_blogger_email": "tamatave.delestage@gmail.com",
        "contact_manager_name": "Coordination Atsinanana",
        "contact_manager_phone": "",
        "contact_manager_email": "",
        "platforms": [
            {
                "platform_name": "Facebook",
                "url": "https://www.facebook.com/tamatave.tsy.manaiky.delestage",
                "handle": "@tamatave.tsy.manaiky.delestage",
                "followers_count": 37000,
                "posts_count": 390,
                "channel_description": "Grassroots citizen collective of Toamasina confronting JIRAMA power cuts and municipal paralysis.",
                "engagement_metrics": {
                    "er": "6.8%",
                    "avg_views": "21k"
                }
            }
        ]
    },
    {
        "entity_id": "collectif_mahajanga_tsy_matory",
        "full_name": "Collectif Mahajanga Tsy Matory",
        "alias": "Mahajanga Tsy Matory (Anti-Coupures)",
        "gender": "Group",
        "residency_status": "Resident",
        "country": "Madagascar",
        "region": "Boeny",
        "city": "Mahajanga",
        "is_foreign_guest": False,
        "is_humanitarian": False,
        "category_main": "Политика, расследования и гражданский протест",
        "category_sub": "Гражданский протест и кризис JIRAMA",
        "tags": "Mahajanga, Majunga, Boeny, JIRAMA, Heatwave, Civil Disobedience, Public Outrage",
        "persona_role": "Гражданский комитет сопротивления города Махадзанга (Маджунга) против многочасовых отключений электричества в условиях экстремальной тропической жары",
        "content_topics": "Гуманитарные последствия отключений вентиляции и холодильных установок при 40-градусной жаре, демонстрации у регионального отделения JIRAMA в Махабибо и Царарано, забастовки гостиничного сектора",
        "target_audience": "Население региона Буэни, работники туризма и рыболовства, студенты кампуса Амбундруна",
        "primary_language": "Малагасийский",
        "llm_description": "Collectif Mahajanga Tsy Matory ('Mahajanga Does Not Sleep') mobilizes citizens in western Madagascar enduring up to 18 hours of daily power outages amid oppressive heatwaves. The movement combines sit-ins outside regional JIRAMA distribution centers with economic boycotts, drawing massive backing from local fisheries and tourism workers.",
        "contact_blogger_phone": "",
        "contact_blogger_email": "mahajanga.tsymatory@gmail.com",
        "contact_manager_name": "Comité de Vigilance Boeny",
        "contact_manager_phone": "",
        "contact_manager_email": "",
        "platforms": [
            {
                "platform_name": "Facebook",
                "url": "https://www.facebook.com/mahajanga.tsymatory.jirama",
                "handle": "@mahajanga.tsymatory.jirama",
                "followers_count": 29500,
                "posts_count": 340,
                "channel_description": "Civic front against blackouts, water cuts, and public utility collapse in Mahajanga.",
                "engagement_metrics": {
                    "er": "6.5%",
                    "avg_views": "17k"
                }
            }
        ]
    },
    {
        "entity_id": "collectif_diego_tsy_manaiky_maizina",
        "full_name": "Collectif Diego Tsy Manaiky Maizina",
        "alias": "Diego Tsy Manaiky Maizina (Antsiranana)",
        "gender": "Group",
        "residency_status": "Resident",
        "country": "Madagascar",
        "region": "Diana",
        "city": "Antsiranana",
        "is_foreign_guest": False,
        "is_humanitarian": False,
        "category_main": "Политика, расследования и гражданский протест",
        "category_sub": "Гражданский протест и кризис JIRAMA",
        "tags": "Diego-Suarez, Antsiranana, Diana, JIRAMA, Northern Madagascar, Energy Crisis, Street Protests",
        "persona_role": "Гражданский альянс жителей Анцирананы (Диего-Суарес) против блэкаутов, вызванных нехваткой мазута и спорами с частными поставщиками энергии (ENELEC)",
        "content_topics": "Требования раскрытия тайных контрактов с частными генераторными операторами, освещение отключений в городских больницах и школах, организация ночных кастрюльных бунтов (casserolades)",
        "target_audience": "Жители провинции Диана, медики, портовые служащие, молодежь Анцирананы",
        "primary_language": "Малагасийский",
        "llm_description": "Collectif Diego Tsy Manaiky Maizina coordinates civilian protests in northern Madagascar's largest port city, Antsiranana. In response to prolonged blackouts threatening hospital operations and regional trade, the movement stages noisy nighttime casserole protests and demands direct state accountability for private generator fuel shortages.",
        "contact_blogger_phone": "",
        "contact_blogger_email": "diego.tsymanaiky@gmail.com",
        "contact_manager_name": "Coordination Diana",
        "contact_manager_phone": "",
        "contact_manager_email": "",
        "platforms": [
            {
                "platform_name": "Facebook",
                "url": "https://www.facebook.com/antsiranana.diego.delestage",
                "handle": "@antsiranana.diego.delestage",
                "followers_count": 27000,
                "posts_count": 310,
                "channel_description": "Official voice of Antsiranana citizens fighting against endless electricity blackouts and water penury.",
                "engagement_metrics": {
                    "er": "6.1%",
                    "avg_views": "16k"
                }
            }
        ]
    },
    {
        "entity_id": "clovis_razafimalala",
        "full_name": "Clovis Razafimalala",
        "alias": "Clovis Razafimalala (Lampogno Maroantsetra)",
        "gender": "Male",
        "residency_status": "Resident",
        "country": "Madagascar",
        "region": "Analanjirofo",
        "city": "Maroantsetra",
        "is_foreign_guest": False,
        "is_humanitarian": False,
        "category_main": "Политика, расследования и гражданский протест",
        "category_sub": "Гражданский протест и кризис JIRAMA",
        "tags": "Whistleblower, Environmental Defender, Rosewood, Maroantsetra, Civic Courage, Human Rights",
        "persona_role": "Известный малагасийский эколог, антикоррупционный разоблачитель, президент коалиции Lampogno в Маруанцетре, лауреат международных премий за защиту прав человека",
        "content_topics": "Разоблачение мафии по контрабанде розового дерева и ванили, разоблачение политиков-покровителей незаконных рубок в национальном парке Масуала, защита коммунальных прав местных общин",
        "target_audience": "Международные экологические организации, правозащитники Amnesty и Global Witness, местное население северо-востока Мадагаскара",
        "primary_language": "Малагасийский",
        "llm_description": "Clovis Razafimalala is an iconic environmental whistleblower and human rights defender from Maroantsetra. Having survived arbitrary detention for exposing illicit rosewood trafficking syndicates linked to political elites, he leads the Lampogno coalition, courageously campaigning against natural resource pillage and systemic civic abandonment in northeastern Madagascar.",
        "contact_blogger_phone": "",
        "contact_blogger_email": "clovis.razafimalala@gmail.com",
        "contact_manager_name": "Coalition Lampogno",
        "contact_manager_phone": "",
        "contact_manager_email": "",
        "platforms": [
            {
                "platform_name": "Facebook",
                "url": "https://www.facebook.com/clovis.razafimalala.whistleblower",
                "handle": "@clovis.razafimalala.whistleblower",
                "followers_count": 21000,
                "posts_count": 380,
                "channel_description": "Whistleblowing investigations on rosewood cartels, rainforest protection, and grassroots community defense.",
                "engagement_metrics": {
                    "er": "5.9%",
                    "avg_views": "13k"
                }
            }
        ]
    },
    {
        "entity_id": "pasteur_marc_tatandraza",
        "full_name": "Marc Tatandraza",
        "alias": "Pasteur Tatandraza (Voie de la Vérité)",
        "gender": "Male",
        "residency_status": "Resident",
        "country": "Madagascar",
        "region": "Atsinanana",
        "city": "Toamasina",
        "is_foreign_guest": False,
        "is_humanitarian": False,
        "category_main": "Политика, расследования и гражданский протест",
        "category_sub": "Гражданский протест и кризис JIRAMA",
        "tags": "Social Protest, Religious Leadership, Grassroots Mobilization, Toamasina, Poverty Crisis, Human Rights",
        "persona_role": "Религиозный лидер, харизматичный народный трибун и общественный деятель, организующий массовые молитвенные и социальные сходы против обнищания населения",
        "content_topics": "Критика правящего режима с позиций социальной справедливости, обличение морального и экономического разложения элит, защита беднейших слоев населения от репрессий",
        "target_audience": "Верующие протестантских и евангельских общин, малообеспеченные слои восточных и южных регионов, сторонники социальных перемен",
        "primary_language": "Малагасийский",
        "llm_description": "Pasteur Marc Tatandraza is an outspoken, controversial religious figure and grassroots social mobilizer based in eastern Madagascar. Combining spiritual oratory with fierce denouncements of state poverty, utility deprivation, and political oppression, his assemblies draw massive crowds of working-class citizens seeking systemic change.",
        "contact_blogger_phone": "",
        "contact_blogger_email": "contact.tatandraza@gmail.com",
        "contact_manager_name": "Secrétariat Ministère Tatandraza",
        "contact_manager_phone": "",
        "contact_manager_email": "",
        "platforms": [
            {
                "platform_name": "Facebook",
                "url": "https://www.facebook.com/pasteur.tatandraza.officiel",
                "handle": "@pasteur.tatandraza.officiel",
                "followers_count": 68000,
                "posts_count": 520,
                "channel_description": "Sermons on social justice, community solidarity, and critiques of state governance by Pasteur Marc Tatandraza.",
                "engagement_metrics": {
                    "er": "6.3%",
                    "avg_views": "31k"
                }
            }
        ]
    },
    {
        "entity_id": "mouvement_mba_rariny",
        "full_name": "Mouvement Mba Rariny",
        "alias": "Mba Rariny (Justice Énergétique & Sociale)",
        "gender": "Group",
        "residency_status": "Resident",
        "country": "Madagascar",
        "region": "Analamanga",
        "city": "Antananarivo",
        "is_foreign_guest": False,
        "is_humanitarian": False,
        "category_main": "Политика, расследования и гражданский протест",
        "category_sub": "Гражданский протест и кризис JIRAMA",
        "tags": "JIRAMA, Social Justice, Slum Rights, Public Utility Equality, Antananarivo, Citizen Action",
        "persona_role": "Гражданское движение за социальную справедливость и равенство доступа к базовым услугам (воде, свету, медицине) в неблагополучных кварталах Антананариву",
        "content_topics": "Защита жителей трущобных зон от отключений общественных колонок с питьевой водой, мониторинг тарифов на электроэнергию для малоимущих, противодействие полицейскому насилию",
        "target_audience": "Обитатели бедных кварталов столицы, поденные рабочие, матери-одиночки, социально уязвимые граждане",
        "primary_language": "Малагасийский",
        "llm_description": "Mouvement Mba Rariny ('Let There Be Fairness') is a grassroots civil society organization fighting energy poverty and structural discrimination in Antananarivo's most marginalized fokontany. The movement stages peaceful sit-ins, documents infant health crises provoked by water pump closures, and advocates for universal lifeline utility quotas.",
        "contact_blogger_phone": "",
        "contact_blogger_email": "mbarariny.madagascar@gmail.com",
        "contact_manager_name": "Comité Directeur Mba Rariny",
        "contact_manager_phone": "",
        "contact_manager_email": "",
        "platforms": [
            {
                "platform_name": "Facebook",
                "url": "https://www.facebook.com/mouvement.mbarariny",
                "handle": "@mouvement.mbarariny",
                "followers_count": 32000,
                "posts_count": 360,
                "channel_description": "Fighting for fair public utilities, water access, and dignity in Madagascar's underserved communities.",
                "engagement_metrics": {
                    "er": "5.7%",
                    "avg_views": "18k"
                }
            }
        ]
    },
    {
        "entity_id": "collectif_antsirabe_vahoaka_miray",
        "full_name": "Collectif Vahoaka Miray Antsirabe",
        "alias": "Vahoaka Miray Antsirabe",
        "gender": "Group",
        "residency_status": "Resident",
        "country": "Madagascar",
        "region": "Vakinankaratra",
        "city": "Antsirabe",
        "is_foreign_guest": False,
        "is_humanitarian": False,
        "category_main": "Политика, расследования и гражданский протест",
        "category_sub": "Гражданский протест и кризис JIRAMA",
        "tags": "Antsirabe, Vakinankaratra, Industry, JIRAMA, Blackout, Textile Workers, Local Economy",
        "persona_role": "Объединение ремесленников, рабочих текстильной промышленности и жителей Анцирабе против блэкаутов, разрушающих промышленное сердце Мадагаскара",
        "content_topics": "Массовые увольнения на текстильных фабриках из-за отсутствия электричества, банкротство ремесленных мастерских по обработке камней и дерева, митинги у мэрии Анцирабе",
        "target_audience": "Рабочие промышленных зон Вакинанкаратра, мелкие предприниматели, водители рикш (Pousse-pousse), жители Анцирабе",
        "primary_language": "Малагасийский",
        "llm_description": "Collectif Vahoaka Miray Antsirabe unifies factory laborers, agricultural processors, and artisans in Madagascar's manufacturing hub of Antsirabe. Facing catastrophic economic losses from unscheduled industrial blackout sequences, the collective mobilizes public pressure demanding uninterrupted hydro-power feeds from Mandraka and Andekaleka stations.",
        "contact_blogger_phone": "",
        "contact_blogger_email": "vahoakamiray.antsirabe@gmail.com",
        "contact_manager_name": "Bureau de Liaison Vakinankaratra",
        "contact_manager_phone": "",
        "contact_manager_email": "",
        "platforms": [
            {
                "platform_name": "Facebook",
                "url": "https://www.facebook.com/antsirabe.vahoaka.miray",
                "handle": "@antsirabe.vahoaka.miray",
                "followers_count": 25500,
                "posts_count": 290,
                "channel_description": "United citizens and workers of Antsirabe demanding electrical stability and economic survival.",
                "engagement_metrics": {
                    "er": "5.5%",
                    "avg_views": "14k"
                }
            }
        ]
    },
    {
        "entity_id": "fenohery_ralambomanana",
        "full_name": "Fenohery Ralambomanana",
        "alias": "Fenohery Ralambomanana (Voix de la Jeunesse Antananarivo)",
        "gender": "Male",
        "residency_status": "Resident",
        "country": "Madagascar",
        "region": "Analamanga",
        "city": "Antananarivo",
        "is_foreign_guest": False,
        "is_humanitarian": False,
        "category_main": "Политика, расследования и гражданский протест",
        "category_sub": "Гражданский протест и кризис JIRAMA",
        "tags": "Youth Voice, Antananarivo, JIRAMA, Urban Resistance, Digital Creator, Civic Mobilization",
        "persona_role": "Молодежный активист, видеоблогер и депутат оппозиционной платформы, ведущий хронику коммунального коллапса и организующий молодежные митинги в Антананариву",
        "content_topics": "Интервью с владельцами малых бизнесов, разорившихся из-за отсутствия электричества, репортажи о забастовках студентов, разоблачение фейковых заявлений министра энергетики",
        "target_audience": "Молодые городские предприниматели, фрилансеры, студенты, активные пользователи Facebook и TikTok",
        "primary_language": "Малагасийский",
        "llm_description": "Fenohery Ralambomanana bridges social media influencer journalism and direct civic protest leadership. Producing high-impact video dispatches revealing the devastation caused by power blackouts on young entrepreneurs, he has become a leading digital spokesperson during municipal demonstrations across the capital.",
        "contact_blogger_phone": "",
        "contact_blogger_email": "fenohery.ralambomanana@gmail.com",
        "contact_manager_name": "Équipe Fenohery Média",
        "contact_manager_phone": "",
        "contact_manager_email": "",
        "platforms": [
            {
                "platform_name": "Facebook",
                "url": "https://www.facebook.com/fenohery.ralambomanana",
                "handle": "@fenohery.ralambomanana",
                "followers_count": 44000,
                "posts_count": 420,
                "channel_description": "Youth civic mobilization, real-life reports on urban blackouts, and social accountability dispatches.",
                "engagement_metrics": {
                    "er": "6.7%",
                    "avg_views": "26k"
                }
            }
        ]
    },

    # =========================================================================
    # 3. СТУДЕНЧЕСКИЙ АКТИВИЗМ И ПРОФСОЮЗЫ (13 ENTITIES)
    # =========================================================================
    {
        "entity_id": "sammy_gregoire_ravelonirina",
        "full_name": "Prof. Sammy Grégoire Ravelonirina",
        "alias": "Prof. Sammy Grégoire (Président SECES Antananarivo)",
        "gender": "Male",
        "residency_status": "Resident",
        "country": "Madagascar",
        "region": "Analamanga",
        "city": "Antananarivo",
        "is_foreign_guest": False,
        "is_humanitarian": False,
        "category_main": "Политика, расследования и гражданский протест",
        "category_sub": "Студенческий активизм и профсоюзы",
        "tags": "SECES, Ankatso, University Union, Strike Leader, Academic Freedom, Higher Education",
        "persona_role": "Президент секции Антананариву профсоюза преподавателей-исследователей высшей школы (SECES Section Antananarivo), лидер общеуниверситетских забастовок в кампусе Анкацу",
        "content_topics": "Забастовки преподавателей высшей школы, невыплата научных надбавок и пенсий, катастрофическое состояние кампуса Анкацу (отсутствие воды и света в лабораториях), критика коммерциализации образования",
        "target_audience": "Профессорско-преподавательский состав 6 университетов Мадагаскара, студенчество, чиновники MESUPRES, профсоюзные лидеры",
        "primary_language": "Малагасийский",
        "llm_description": "Professor Sammy Grégoire Ravelonirina is the influential President of SECES Antananarivo, representing faculty and researchers at Madagascar's flagship University of Antananarivo (Ankatso). Renowned for his uncompromising stances during national academic strikes, he relentlessly confronts the Ministry of Higher Education over unpaid research allocations and campus infrastructural collapse.",
        "contact_blogger_phone": "",
        "contact_blogger_email": "sammy.ravelonirina@univ-antananarivo.mg",
        "contact_manager_name": "Bureau Exécutif SECES Ankatso",
        "contact_manager_phone": "",
        "contact_manager_email": "seces.tana@gmail.com",
        "platforms": [
            {
                "platform_name": "Facebook",
                "url": "https://www.facebook.com/sammygregoire.ravelonirina.seces",
                "handle": "@sammygregoire.ravelonirina.seces",
                "followers_count": 28000,
                "posts_count": 390,
                "channel_description": "Official communication of Prof. Sammy Grégoire Ravelonirina: SECES union communiqués, academic strike updates, and university defense.",
                "engagement_metrics": {
                    "er": "5.6%",
                    "avg_views": "18k"
                }
            }
        ]
    },
    {
        "entity_id": "dimby_ralambomanana",
        "full_name": "Dr. Dimby Ralambomanana",
        "alias": "Dr. Dimby Ralambomanana (Ex-Président SECES National)",
        "gender": "Male",
        "residency_status": "Resident",
        "country": "Madagascar",
        "region": "Analamanga",
        "city": "Antananarivo",
        "is_foreign_guest": False,
        "is_humanitarian": False,
        "category_main": "Политика, расследования и гражданский протест",
        "category_sub": "Студенческий активизм и профсоюзы",
        "tags": "SECES National, Higher Education, Academic Reform, Public Sector Unions, Research Defense",
        "persona_role": "Бывший национальный президент SECES Madagascar, ведущий ученый-исследователь, аналитик профсоюзного движения и университетских кризисов",
        "content_topics": "Стратегия национального профсоюзного диалога, межвузовская солидарность (Антананариву, Туамасина, Махадзанга, Тулиара, Фианаранцуа, Анциранана), защита автономии университетов",
        "target_audience": "Академическое сообщество, исследователи Национального центра научных исследований (CNRE/CNRIT), научная общественность",
        "primary_language": "Французский",
        "llm_description": "Dr. Dimby Ralambomanana served as National President of SECES, coordinating union actions across all public universities and research institutes nationwide. An authoritative voice on university pedagogy and public sector labor law, he publishes strategic white papers addressing the chronic underfunding of scientific research and higher education.",
        "contact_blogger_phone": "",
        "contact_blogger_email": "dimby.ralambomanana@cnre.mg",
        "contact_manager_name": "Secrétariat Permanent SECES National",
        "contact_manager_phone": "",
        "contact_manager_email": "",
        "platforms": [
            {
                "platform_name": "Facebook",
                "url": "https://www.facebook.com/dimby.ralambomanana.seces",
                "handle": "@dimby.ralambomanana.seces",
                "followers_count": 16500,
                "posts_count": 280,
                "channel_description": "Academic labor analyses, national university policies, and research union manifestos.",
                "engagement_metrics": {
                    "er": "4.3%",
                    "avg_views": "9k"
                }
            }
        ]
    },
    {
        "entity_id": "seces_section_antananarivo",
        "full_name": "SECES Section Antananarivo",
        "alias": "SECES Ankatso",
        "gender": "Group",
        "residency_status": "Resident",
        "country": "Madagascar",
        "region": "Analamanga",
        "city": "Antananarivo",
        "is_foreign_guest": False,
        "is_humanitarian": False,
        "category_main": "Политика, расследования и гражданский протест",
        "category_sub": "Студенческий активизм и профсоюзы",
        "tags": "SECES, Ankatso, Union, Faculty Strike, University Crisis, Higher Education, Antananarivo",
        "persona_role": "Официальный цифровой орган профсоюза преподавателей и исследователей университета Антананариву (кампус Анкацу)",
        "content_topics": "Решения генеральных ассамблей профсоюза, ультиматумы правительству по выплате академических задолженностей, отчеты о приостановке занятий и сессий, защита академической неприкосновенности кампуса",
        "target_audience": "Студенты и преподаватели кампуса Анкацу, журналисты образовательных изданий, родительские комитеты",
        "primary_language": "Малагасийский",
        "llm_description": "SECES Section Antananarivo is the official media platform for the most powerful academic union chapter in Madagascar. Based at the iconic Ankatso campus, it publishes the resolutions of general assemblies, orchestrates unified faculty work-stoppages, and releases hard-hitting communiqués regarding higher education governance.",
        "contact_blogger_phone": "",
        "contact_blogger_email": "seces.ankatso.officiel@gmail.com",
        "contact_manager_name": "Bureau de Presse SECES Ankatso",
        "contact_manager_phone": "",
        "contact_manager_email": "",
        "platforms": [
            {
                "platform_name": "Facebook",
                "url": "https://www.facebook.com/seces.section.antananarivo",
                "handle": "@seces.section.antananarivo",
                "followers_count": 54000,
                "posts_count": 610,
                "channel_description": "Official dissemination channel of the Higher Education Teachers and Researchers Union (SECES Antananarivo).",
                "engagement_metrics": {
                    "er": "5.9%",
                    "avg_views": "24k"
                }
            }
        ]
    },
    {
        "entity_id": "seces_national_madagascar",
        "full_name": "SECES National Madagascar",
        "alias": "SECES National",
        "gender": "Group",
        "residency_status": "Resident",
        "country": "Madagascar",
        "region": "Analamanga",
        "city": "Antananarivo",
        "is_foreign_guest": False,
        "is_humanitarian": False,
        "category_main": "Политика, расследования и гражданский протест",
        "category_sub": "Студенческий активизм и профсоюзы",
        "tags": "SECES National, Higher Education, Academic Research, National Strike, Public Universities",
        "persona_role": "Федеральный координирующий орган профсоюза исследователей и преподавателей всех государственных университетов Мадагаскара",
        "content_topics": "Координация всеобщей университетской забастовки в 6 провинциях, мониторинг выполнения правительственных соглашений, защита прав ученых и независимости научного сообщества",
        "target_audience": "Преподаватели университетов Тоамасины, Махадзанги, Тулиары, Фианаранцуа, Анцирананы и Антананариву, Министерство высшего образования",
        "primary_language": "Французский",
        "llm_description": "SECES National Madagascar coordinates union strategy across Madagascar's public university system and national research centers. The federal executive bureau articulates collective bargaining mandates, coordinates nationwide strike declarations, and dialogues with the presidency to preserve public academic institutions.",
        "contact_blogger_phone": "",
        "contact_blogger_email": "seces.national.bureau@gmail.com",
        "contact_manager_name": "Secrétariat Général SECES National",
        "contact_manager_phone": "",
        "contact_manager_email": "",
        "platforms": [
            {
                "platform_name": "Facebook",
                "url": "https://www.facebook.com/seces.national.madagascar",
                "handle": "@seces.national.madagascar",
                "followers_count": 42000,
                "posts_count": 480,
                "channel_description": "Official federal page of SECES National: coordinating academic union resistance across all 6 public universities.",
                "engagement_metrics": {
                    "er": "5.2%",
                    "avg_views": "19k"
                }
            }
        ]
    },
    {
        "entity_id": "mafami_ankatso",
        "full_name": "MAFAMI Ankatso",
        "alias": "MAFAMI (Mpianatra Avy amin'ny Faritra Atsimo Miray)",
        "gender": "Group",
        "residency_status": "Resident",
        "country": "Madagascar",
        "region": "Analamanga",
        "city": "Antananarivo",
        "is_foreign_guest": False,
        "is_humanitarian": False,
        "category_main": "Политика, расследования и гражданский протест",
        "category_sub": "Студенческий активизм и профсоюзы",
        "tags": "MAFAMI, Ankatso, Student Union, Grand Sud, Scholarship Strike, Bourses, University Campus",
        "persona_role": "Влиятельное студенческое землячество выходцев из южных регионов (Андруй, Ануси, Ациму-Андрефана) в университете Антананариву, ударная сила студенческих протестов",
        "content_topics": "Забастовки за своевременную выплату стипендий (bourses) и пособий на учебное оборудование, борьба против выселения из студенческих общежитий Анкацу, защита студентов из засушливого Юга",
        "target_audience": "Студенты университета Антананариву, уроженцы южных провинций, молодежные профсоюзные лидеры",
        "primary_language": "Малагасийский",
        "llm_description": "MAFAMI (Mpianatra Avy amin'ny Faritra Atsimo Miray) is historically the most militant and mobilized regional student association on the Ankatso university campus. Representing students from Madagascar's severely impoverished southern districts, MAFAMI regularly initiates campus-wide walkouts, barricades, and demonstrations over delayed stipends and living conditions.",
        "contact_blogger_phone": "",
        "contact_blogger_email": "mafami.ankatso@gmail.com",
        "contact_manager_name": "Bureau Exécutif MAFAMI",
        "contact_manager_phone": "",
        "contact_manager_email": "",
        "platforms": [
            {
                "platform_name": "Facebook",
                "url": "https://www.facebook.com/mafami.ankatso.officiel",
                "handle": "@mafami.ankatso.officiel",
                "followers_count": 31000,
                "posts_count": 350,
                "channel_description": "Official community platform of southern students at Ankatso University: student welfare, stipend demands, and solidarity.",
                "engagement_metrics": {
                    "er": "7.1%",
                    "avg_views": "20k"
                }
            }
        ]
    },
    {
        "entity_id": "aed_ankatso_droit",
        "full_name": "Association des Étudiants en Droit d'Ankatso",
        "alias": "AED Ankatso (Faculté DEGS / Droit)",
        "gender": "Group",
        "residency_status": "Resident",
        "country": "Madagascar",
        "region": "Analamanga",
        "city": "Antananarivo",
        "is_foreign_guest": False,
        "is_humanitarian": False,
        "category_main": "Политика, расследования и гражданский протест",
        "category_sub": "Студенческий активизм и профсоюзы",
        "tags": "AED, Law Students, FDSP, Ankatso, Constitutional Rights, Student Council, Legal Defense",
        "persona_role": "Студенческая ассоциация факультета права и политологии (FDSP) университета Антананариву, организатор правовых дебатов и студенческих деклараций по конституционному кризису",
        "content_topics": "Юридический анализ избирательных законов, правовое просвещение студентов, защита студентов от неправомерных задержаний силами жандармерии на территории кампуса",
        "target_audience": "Студенты-юристы, молодые магистры права, практикующие адвокаты, гражданские активисты",
        "primary_language": "Смешанный",
        "llm_description": "Association des Étudiants en Droit d'Ankatso (AED) serves as the primary representative body for law and political science students at the University of Antananarivo. The association actively publishes legal critiques on constitutional breaches, stages mock tribunals on state corruption, and organizes legal defense teams when campus protesters face arrest.",
        "contact_blogger_phone": "",
        "contact_blogger_email": "aed.ankatso@gmail.com",
        "contact_manager_name": "Présidence AED Ankatso",
        "contact_manager_phone": "",
        "contact_manager_email": "",
        "platforms": [
            {
                "platform_name": "Facebook",
                "url": "https://www.facebook.com/aed.ankatso.droit",
                "handle": "@aed.ankatso.droit",
                "followers_count": 27500,
                "posts_count": 310,
                "channel_description": "Law students of Ankatso: constitutional awareness, academic defense, and legal student forums.",
                "engagement_metrics": {
                    "er": "5.3%",
                    "avg_views": "13k"
                }
            }
        ]
    },
    {
        "entity_id": "aes_ankatso_sciences",
        "full_name": "Association des Étudiants en Sciences d'Ankatso",
        "alias": "AES Ankatso (Faculté des Sciences)",
        "gender": "Group",
        "residency_status": "Resident",
        "country": "Madagascar",
        "region": "Analamanga",
        "city": "Antananarivo",
        "is_foreign_guest": False,
        "is_humanitarian": False,
        "category_main": "Политика, расследования и гражданский протест",
        "category_sub": "Студенческий активизм и профсоюзы",
        "tags": "AES, Sciences, Ankatso, Lab Infrastructure, Energy Penury, Student Union",
        "persona_role": "Студенческий совет факультета естественных наук университета Антананариву, активный участник университетских протестов против разрушения лабораторий и блэкаутов",
        "content_topics": "Протесты против отключения электричества в исследовательских лабораториях, уничтожение экспериментальных биологических культур из-за блэкаутов, требования оснащения кампуса",
        "target_audience": "Студенты-биологи, химики, физики, математики, молодые исследователи, техническая интеллигенция",
        "primary_language": "Малагасийский",
        "llm_description": "Association des Étudiants en Sciences d'Ankatso (AES) organizes students across the physical, biological, and mathematical sciences at Ankatso. The association is at the forefront of campus demonstrations highlighting how JIRAMA's recurring power outages destroy irreplaceable scientific laboratory samples, incubators, and computing assets.",
        "contact_blogger_phone": "",
        "contact_blogger_email": "aes.sciences.ankatso@gmail.com",
        "contact_manager_name": "Bureau AES Ankatso",
        "contact_manager_phone": "",
        "contact_manager_email": "",
        "platforms": [
            {
                "platform_name": "Facebook",
                "url": "https://www.facebook.com/aes.ankatso.sciences",
                "handle": "@aes.ankatso.sciences",
                "followers_count": 22000,
                "posts_count": 290,
                "channel_description": "Science students of Ankatso University: laboratory rights, stipend claims, and scientific community alerts.",
                "engagement_metrics": {
                    "er": "5.1%",
                    "avg_views": "11k"
                }
            }
        ]
    },
    {
        "entity_id": "etudiants_barikadimy_toamasina",
        "full_name": "Collectif des Étudiants de l'Université de Barikadimy",
        "alias": "Étudiants Barikadimy Toamasina",
        "gender": "Group",
        "residency_status": "Resident",
        "country": "Madagascar",
        "region": "Atsinanana",
        "city": "Toamasina",
        "is_foreign_guest": False,
        "is_humanitarian": False,
        "category_main": "Политика, расследования и гражданский протест",
        "category_sub": "Студенческий активизм и профсоюзы",
        "tags": "Barikadimy, Toamasina, University of Toamasina, Student Strike, Coastal Youth, Bourses",
        "persona_role": "Общеуниверситетский союз студентов кампуса Барикадими (Университет Туамасины), организующий протесты на восточном побережье Мадагаскара",
        "content_topics": "Задержка стипендий, катастрофическое отсутствие питьевой воды в университетском городке Барикадими, протесты против произвола университетской администрации, координация с бастующими докерами",
        "target_audience": "Студенчество провинции Туамасина, молодежь региона Ацинанана, преподаватели университета",
        "primary_language": "Малагасийский",
        "llm_description": "Collectif des Étudiants de l'Université de Barikadimy represents the vibrant student population of Toamasina University. Known for staging massive blockades of the RN2 highway when student bursaries are withheld or campus water supplies are cut, the collective constitutes one of the most assertive regional civic forces outside the capital.",
        "contact_blogger_phone": "",
        "contact_blogger_email": "etudiants.barikadimy@gmail.com",
        "contact_manager_name": "Coordination Générale Barikadimy",
        "contact_manager_phone": "",
        "contact_manager_email": "",
        "platforms": [
            {
                "platform_name": "Facebook",
                "url": "https://www.facebook.com/etudiants.barikadimy.toamasina",
                "handle": "@etudiants.barikadimy.toamasina",
                "followers_count": 35000,
                "posts_count": 380,
                "channel_description": "Official student solidarity platform of Barikadimy Campus (University of Toamasina): welfare and resistance dispatches.",
                "engagement_metrics": {
                    "er": "6.6%",
                    "avg_views": "20k"
                }
            }
        ]
    },
    {
        "entity_id": "etudiants_maninday_toliara",
        "full_name": "Association des Étudiants de l'Université de Maninday",
        "alias": "Étudiants Maninday Toliara",
        "gender": "Group",
        "residency_status": "Resident",
        "country": "Madagascar",
        "region": "Atsimo-Andrefana",
        "city": "Toliara",
        "is_foreign_guest": False,
        "is_humanitarian": False,
        "category_main": "Политика, расследования и гражданский протест",
        "category_sub": "Студенческий активизм и профсоюзы",
        "tags": "Maninday, Toliara, University of Toliara, Student Rights, Water Penury, South Madagascar",
        "persona_role": "Студенческая организация кампуса Маниндай (Университет Тулиары), ведущая борьбу за права студентов юго-западных регионов Мадагаскара",
        "content_topics": "Кризис снабжения пресной водой в кампусе Маниндай, нерегулярность выплаты стипендий, нехватка преподавательских кадров, протесты против подорожания транспорта до города",
        "target_audience": "Студенты и выпускники университета Тулиары, жители юго-запада, образовательные ассоциации",
        "primary_language": "Малагасийский",
        "llm_description": "Association des Étudiants de l'Université de Maninday represents students at the University of Toliara. Confronting severe regional isolation and desert water scarcity, the association regularly conducts student demonstrations to demand basic potable cistern trucks, internet access for study halls, and equitable distribution of national research budgets.",
        "contact_blogger_phone": "",
        "contact_blogger_email": "etudiants.maninday@gmail.com",
        "contact_manager_name": "Bureau des Étudiants Maninday",
        "contact_manager_phone": "",
        "contact_manager_email": "",
        "platforms": [
            {
                "platform_name": "Facebook",
                "url": "https://www.facebook.com/etudiants.maninday.toliara",
                "handle": "@etudiants.maninday.toliara",
                "followers_count": 26000,
                "posts_count": 320,
                "channel_description": "Official voice of Maninday University campus in Toliara: student rights, bursary distribution, and regional equity.",
                "engagement_metrics": {
                    "er": "6.3%",
                    "avg_views": "15k"
                }
            }
        ]
    },
    {
        "entity_id": "etudiants_ambondrona_mahajanga",
        "full_name": "Solidarité des Étudiants d'Ambondrona",
        "alias": "Étudiants Ambondrona Mahajanga",
        "gender": "Group",
        "residency_status": "Resident",
        "country": "Madagascar",
        "region": "Boeny",
        "city": "Mahajanga",
        "is_foreign_guest": False,
        "is_humanitarian": False,
        "category_main": "Политика, расследования и гражданский протест",
        "category_sub": "Студенческий активизм и профсоюзы",
        "tags": "Ambondrona, Mahajanga, University of Mahajanga, Health Sciences, Campus Strike, Boeny",
        "persona_role": "Студенческий координационный совет кампуса Амбундруна (Университет Махадзанги, включая медицинский и стоматологический факультеты)",
        "content_topics": "Протесты студентов-медиков против нехватки оборудования в университетском госпитале CHU Mahajanga, перебои со светом во время хирургических практик, задержка интернских стипендий",
        "target_audience": "Студенты-медики, интерны, преподаватели университета Махадзанги, ассоциации врачей",
        "primary_language": "Малагасийский",
        "llm_description": "Solidarité des Étudiants d'Ambondrona unifies medical, dental, and multidisciplinary students at the University of Mahajanga's Ambondrona campus. Renowned for its articulate advocacy, the union stages rallies protesting how regional JIRAMA blackouts paralyze dental autoclaves and university hospital teaching clinics.",
        "contact_blogger_phone": "",
        "contact_blogger_email": "ambondrona.etudiants@gmail.com",
        "contact_manager_name": "Bureau de Coordination Ambondrona",
        "contact_manager_phone": "",
        "contact_manager_email": "",
        "platforms": [
            {
                "platform_name": "Facebook",
                "url": "https://www.facebook.com/etudiants.ambondrona.mahajanga",
                "handle": "@etudiants.ambondrona.mahajanga",
                "followers_count": 23500,
                "posts_count": 280,
                "channel_description": "Campus Ambondrona student representation: medical intern rights, bursary transparency, and university welfare in Mahajanga.",
                "engagement_metrics": {
                    "er": "5.8%",
                    "avg_views": "13k"
                }
            }
        ]
    },
    {
        "entity_id": "etudiants_andrainjato_fianarantsoa",
        "full_name": "Collectif des Étudiants d'Andrainjato",
        "alias": "Étudiants Andrainjato Fianarantsoa",
        "gender": "Group",
        "residency_status": "Resident",
        "country": "Madagascar",
        "region": "Haute Matsiatra",
        "city": "Fianarantsoa",
        "is_foreign_guest": False,
        "is_humanitarian": False,
        "category_main": "Политика, расследования и гражданский протест",
        "category_sub": "Студенческий активизм и профсоюзы",
        "tags": "Andrainjato, Fianarantsoa, ENI, Computer Science, Higher Education, Student Strike",
        "persona_role": "Студенческий союз кампуса Андраинджато (Университет Фианаранцуа, включая знаменитую Национальную школу информатики ENI)",
        "content_topics": "Защита условий обучения студентов-программистов, блэкауты, разрушающие серверы и компьютерные лаборатории ENI, задержки стипендий, студенческие шествия к префектуре",
        "target_audience": "Студенты IT-специальностей, программисты, преподаватели университета Фианаранцуа",
        "primary_language": "Малагасийский",
        "llm_description": "Collectif des Étudiants d'Andrainjato organizes students at the University of Fianarantsoa, home to Madagascar's prestigious national computer science school (ENI). The collective vocally denounces regional energy deprivation that halts software engineering curriculums, mobilizing regular student strikes across the southern highlands.",
        "contact_blogger_phone": "",
        "contact_blogger_email": "andrainjato.etudiants@gmail.com",
        "contact_manager_name": "Bureau Exécutif Andrainjato",
        "contact_manager_phone": "",
        "contact_manager_email": "",
        "platforms": [
            {
                "platform_name": "Facebook",
                "url": "https://www.facebook.com/etudiants.andrainjato.fianar",
                "handle": "@etudiants.andrainjato.fianar",
                "followers_count": 25000,
                "posts_count": 310,
                "channel_description": "Official communication of Andrainjato Campus students (Fianarantsoa): digital rights, campus electricity, and bursaries.",
                "engagement_metrics": {
                    "er": "6.0%",
                    "avg_views": "14k"
                }
            }
        ]
    },
    {
        "entity_id": "etudiants_espa_vontovorona",
        "full_name": "Association des Étudiants de l'ESPA Vontovorona",
        "alias": "ESPA Vontovorona Polytechnique",
        "gender": "Group",
        "residency_status": "Resident",
        "country": "Madagascar",
        "region": "Analamanga",
        "city": "Antananarivo",
        "is_foreign_guest": False,
        "is_humanitarian": False,
        "category_main": "Политика, расследования и гражданский протест",
        "category_sub": "Студенческий активизм и профсоюзы",
        "tags": "Polytechnique, ESPA, Vontovorona, Engineering Students, Road Access, Campus Protests",
        "persona_role": "Студенческая ассоциация Высшей политехнической школы Антананариву (кампус Вунтувуруна), будущая инженерная элита Мадагаскара",
        "content_topics": "Забастовки из-за разрушенной дороги к кампусу Вунтувуруна, отсутствие автобусного сообщения, поломки тяжелых станков и генераторов из-за скачков напряжения JIRAMA",
        "target_audience": "Студенты-инженеры, политехники, выпускники технических вузов, промышленное сообщество",
        "primary_language": "Смешанный",
        "llm_description": "Association des Étudiants de l'ESPA Vontovorona unites engineering students at Madagascar's premier polytechnic institute located in suburban Vontovorona. The association is renowned for its disciplined mass mobilizations over broken transportation corridors, workshop equipment power outages, and student welfare allocations.",
        "contact_blogger_phone": "",
        "contact_blogger_email": "espa.vontovorona.bde@gmail.com",
        "contact_manager_name": "Bureau des Élèves ESPA",
        "contact_manager_phone": "",
        "contact_manager_email": "",
        "platforms": [
            {
                "platform_name": "Facebook",
                "url": "https://www.facebook.com/espa.vontovorona.etudiants",
                "handle": "@espa.vontovorona.etudiants",
                "followers_count": 33000,
                "posts_count": 370,
                "channel_description": "Official student body of Ecole Supérieure Polytechnique d'Antananarivo (Vontovorona): engineering advocacy and student rights.",
                "engagement_metrics": {
                    "er": "5.7%",
                    "avg_views": "17k"
                }
            }
        ]
    },
    {
        "entity_id": "syndicat_magistrats_madagascar",
        "full_name": "Syndicat des Magistrats de Madagascar",
        "alias": "SMM Madagascar",
        "gender": "Group",
        "residency_status": "Resident",
        "country": "Madagascar",
        "region": "Analamanga",
        "city": "Antananarivo",
        "is_foreign_guest": False,
        "is_humanitarian": False,
        "category_main": "Политика, расследования и гражданский протест",
        "category_sub": "Студенческий активизм и профсоюзы",
        "tags": "SMM, Judiciary, Magistrats, Rule of Law, Judicial Independence, Anti-Corruption, Constitutional Order",
        "persona_role": "Профсоюз судей и магистратов Мадагаскара (SMM), ключевая независимая корпорация, выступающая против давления исполнительной власти на правосудие",
        "content_topics": "Защита независимости судей от телефонного права министров, забастовки судов против произвола властей, преследования непокорных прокуроров, борьба с коррупцией в пенитенциарной системе",
        "target_audience": "Судьи, прокуроры, адвокаты коллегии, правозащитные НКО, международные юридические ассоциации",
        "primary_language": "Французский",
        "llm_description": "Syndicat des Magistrats de Madagascar (SMM) is the primary professional union of Malagasy judges and prosecutors. Renowned for historic nationwide judicial strikes, the SMM acts as an essential institutional bulwark defending judicial independence against executive interference, politically motivated prosecutions, and ministerial coercion.",
        "contact_blogger_phone": "",
        "contact_blogger_email": "smm.madagascar.bureau@gmail.com",
        "contact_manager_name": "Bureau Exécutif SMM",
        "contact_manager_phone": "",
        "contact_manager_email": "",
        "platforms": [
            {
                "platform_name": "Facebook",
                "url": "https://www.facebook.com/syndicat.magistrats.madagascar",
                "handle": "@syndicat.magistrats.madagascar",
                "followers_count": 46000,
                "posts_count": 420,
                "channel_description": "Official communication page of the Union of Malagasy Magistrates: defending the separation of powers and judicial integrity.",
                "engagement_metrics": {
                    "er": "5.1%",
                    "avg_views": "21k"
                }
            }
        ]
    },

    # =========================================================================
    # 4. НЕЗАВИСИМЫЕ РАССЛЕДОВАНИЯ И ДИССИДЕНТСТВО (12 ENTITIES)
    # =========================================================================
    {
        "entity_id": "gaby_vakoka",
        "full_name": "Gaby Ratsivalaka",
        "alias": "Gaby Vakoka (Chroniqueur Diaspora Europe)",
        "gender": "Male",
        "residency_status": "Diaspora France",
        "country": "France",
        "region": "Île-de-France",
        "city": "Paris",
        "is_foreign_guest": False,
        "is_humanitarian": False,
        "category_main": "Политика, расследования и гражданский протест",
        "category_sub": "Независимые расследования и диссидентство",
        "tags": "Diaspora, France, Whistleblower, Political Critique, Corruption, Live Debrief, Malagasy Exiles",
        "persona_role": "Политический обозреватель малагасийской диаспоры в Европе, популярный ведущий расследовательских прямых эфиров, критик коррупционных схем мадагаскарских властей",
        "content_topics": "Анализ офшорных активов высокопоставленных чиновников, расследования контрабанды золота через Дубай и Коморы, разоблачение манипуляций в энергетических закупках JIRAMA",
        "target_audience": "Малагасийская диаспора во Франции, Бельгии, Швейцарии, протестная молодежь Мадагаскара, независимые блогеры",
        "primary_language": "Малагасийский",
        "llm_description": "Gaby Ratsivalaka, known online as 'Gaby Vakoka', is an influential France-based diaspora commentator and investigative broadcaster. Conducting hard-hitting, multi-hour Facebook Live debriefs, he dissects high-level state corruption, opaque mining concessions, and the wealth accumulation of the ruling political class.",
        "contact_blogger_phone": "",
        "contact_blogger_email": "gabyvakoka@gmail.com",
        "contact_manager_name": "Production Gaby Vakoka",
        "contact_manager_phone": "",
        "contact_manager_email": "",
        "platforms": [
            {
                "platform_name": "Facebook",
                "url": "https://www.facebook.com/gabyvakoka.officiel",
                "handle": "@gabyvakoka.officiel",
                "followers_count": 86000,
                "posts_count": 670,
                "channel_description": "Investigative political debriefs, whistleblower leaks, and governance critiques by diaspora commentator Gaby Vakoka.",
                "engagement_metrics": {
                    "er": "6.8%",
                    "avg_views": "45k"
                }
            }
        ]
    },
    {
        "entity_id": "jean_luc_raharimanana",
        "full_name": "Jean-Luc Raharimanana",
        "alias": "Raharimanana (Écrivain & Dissident Politique)",
        "gender": "Male",
        "residency_status": "Diaspora France",
        "country": "France",
        "region": "Île-de-France",
        "city": "Paris",
        "is_foreign_guest": False,
        "is_humanitarian": False,
        "category_main": "Политика, расследования и гражданский протест",
        "category_sub": "Независимые расследования и диссидентство",
        "tags": "Dissident, Literature, Political Essayist, Diaspora, Human Rights, Freedom of Speech",
        "persona_role": "Всемирно известный малагасийский писатель, драматург, философ и политический диссидент во Франции, непримиримый критик авторитаризма и неоколониализма",
        "content_topics": "Философский анализ государственного насилия и бедности на Мадагаскаре, защита свободы слова и преследуемых журналистов, историческая память восстания 1947 года",
        "target_audience": "Франкоязычная интеллектуальная элита, международные литературные и правозащитные круги, малагасийские студенты за рубежом",
        "primary_language": "Французский",
        "llm_description": "Jean-Luc Raharimanana is one of Madagascar's foremost literary figures and political essayists living in exile in France. A relentless critic of postcolonial autocracy, political impunity, and violence, his essays, dramatic works, and public interventions provide profound intellectual and ethical backing to the Malagasy democratic opposition.",
        "contact_blogger_phone": "",
        "contact_blogger_email": "raharimanana.contact@gmail.com",
        "contact_manager_name": "Éditions & Diffusion Raharimanana",
        "contact_manager_phone": "",
        "contact_manager_email": "",
        "platforms": [
            {
                "platform_name": "Facebook",
                "url": "https://www.facebook.com/raharimanana.officiel",
                "handle": "@raharimanana.officiel",
                "followers_count": 24000,
                "posts_count": 410,
                "channel_description": "Official page of writer Jean-Luc Raharimanana: political essays, cultural critique, and civil liberties advocacy.",
                "engagement_metrics": {
                    "er": "4.6%",
                    "avg_views": "11k"
                }
            }
        ]
    },
    {
        "entity_id": "lalatiana_pitchboule",
        "full_name": "Lalatiana Pitchboule",
        "alias": "Pitchboule de Paris (Chroniqueuse d'Opposition)",
        "gender": "Female",
        "residency_status": "Diaspora France",
        "country": "France",
        "region": "Île-de-France",
        "city": "Paris",
        "is_foreign_guest": False,
        "is_humanitarian": False,
        "category_main": "Политика, расследования и гражданский протест",
        "category_sub": "Независимые расследования и диссидентство",
        "tags": "Diaspora, France, Whistleblower, Live Streaming, Opposition Critique, Civic Outrage",
        "persona_role": "Популярная ведущая оппозиционных стримов и разоблачительных программ малагасийской диаспоры в Париже, защитница прав малагасийских политзаключенных",
        "content_topics": "Прямые разоблачения коррупционных скандалов в высших эшелонах власти, координация сборов помощи семьям арестованных активистов, комментирование уличных манифестаций в Антананариву",
        "target_audience": "Женская малагасийская аудитория диаспоры, активные пользователи соцсетей в эмиграции, оппозиционные активисты на Мадагаскаре",
        "primary_language": "Малагасийский",
        "llm_description": "Lalatiana Pitchboule is a vibrant, fearless diaspora opinion leader broadcasting from Paris. Her lively, sharp-tongued Facebook Live streams attract tens of thousands of viewers, serving as an unfiltered bulletin for leaks regarding ministerial embezzlement, military abuse, and civil resistance in Antananarivo.",
        "contact_blogger_phone": "",
        "contact_blogger_email": "pitchbouledeparis@gmail.com",
        "contact_manager_name": "Pitchboule Média Production",
        "contact_manager_phone": "",
        "contact_manager_email": "",
        "platforms": [
            {
                "platform_name": "Facebook",
                "url": "https://www.facebook.com/lalatiana.pitchboule",
                "handle": "@lalatiana.pitchboule",
                "followers_count": 72000,
                "posts_count": 590,
                "channel_description": "Diaspora live broadcasts, whistleblowing exposés, and political opposition commentary by Lalatiana Pitchboule.",
                "engagement_metrics": {
                    "er": "6.4%",
                    "avg_views": "39k"
                }
            }
        ]
    },
    {
        "entity_id": "patrick_raharimanana_gtt",
        "full_name": "Patrick Raharimanana",
        "alias": "Patrick Raharimanana (Gasy Tia Tanindrazana)",
        "gender": "Male",
        "residency_status": "Diaspora France",
        "country": "France",
        "region": "Île-de-France",
        "city": "Paris",
        "is_foreign_guest": False,
        "is_humanitarian": False,
        "category_main": "Политика, расследования и гражданский протест",
        "category_sub": "Независимые расследования и диссидентство",
        "tags": "Diaspora, GTT, Economy, Sovereign Debt, Public Finance, Mining Audit, France",
        "persona_role": "Экономист, президент движения патриотической диаспоры 'Gasy Tia Tanindrazana' (GTT International), финансовый эксперт и публицист",
        "content_topics": "Экономический аудит государственных контрактов в горнодобывающей отрасли (Ambatovy, QMM), разоблачение кабальных долговых соглашений JIRAMA, анализ инфляции и курса ариари",
        "target_audience": "Малагасийские финансисты, экономисты, предприниматели диаспоры, академические исследователи развития",
        "primary_language": "Смешанный",
        "llm_description": "Patrick Raharimanana is a Paris-based economist and leader of Gasy Tia Tanindrazana (GTT International). He specializes in forensic economic critiques of Malagasy public finance, exposing sovereign debt mismanagement, resource extraction undervaluation, and the systemic deficits of state-owned enterprises like JIRAMA.",
        "contact_blogger_phone": "",
        "contact_blogger_email": "patrick.raharimanana@gtt-international.org",
        "contact_manager_name": "Secrétariat GTT International",
        "contact_manager_phone": "",
        "contact_manager_email": "",
        "platforms": [
            {
                "platform_name": "Facebook",
                "url": "https://www.facebook.com/patrick.raharimanana.gtt",
                "handle": "@patrick.raharimanana.gtt",
                "followers_count": 38000,
                "posts_count": 520,
                "channel_description": "Macroeconomic audits, sovereignty analysis, and diaspora mobilization for democratic governance in Madagascar.",
                "engagement_metrics": {
                    "er": "4.9%",
                    "avg_views": "17k"
                }
            }
        ]
    },
    {
        "entity_id": "me_willy_razafinjatovo_olala",
        "full_name": "Me Willy Razafinjatovo",
        "alias": "Maître Olala (Doyen des Avocats des Libertés)",
        "gender": "Male",
        "residency_status": "Resident",
        "country": "Madagascar",
        "region": "Analamanga",
        "city": "Antananarivo",
        "is_foreign_guest": False,
        "is_humanitarian": False,
        "category_main": "Политика, расследования и гражданский протест",
        "category_sub": "Независимые расследования и диссидентство",
        "tags": "Maître Olala, Criminal Defense, Barreau, Human Rights, Freedom Defender, Iconic Lawyer",
        "persona_role": "Патриарх малагасийской адвокатуры, легендарный судебный защитник политзаключенных, журналистов и студенческих лидеров, гроза коррумпированных прокуроров",
        "content_topics": "Защита арестованных участников мирных манифестаций, публичные разоблачения пыток в следственных изоляторах (Antanimora), борьба против цензуры и судебного произвола",
        "target_audience": "Адвокаты, судебные журналисты, гражданские активисты, широкая общественность Мадагаскара",
        "primary_language": "Малагасийский",
        "llm_description": "Maître Willy Razafinjatovo, universally known across Madagascar as 'Maître Olala', is an iconic figure in human rights defense and criminal jurisprudence. For decades, he has voluntarily defended opposition politicians, whistleblowers, and impoverished student protesters pro bono, earning unmatched popular respect for confronting executive injustice in courtroom battles.",
        "contact_blogger_phone": "",
        "contact_blogger_email": "willy.razafinjatovo@barreau-madagascar.org",
        "contact_manager_name": "Cabinet Me Willy Razafinjatovo",
        "contact_manager_phone": "",
        "contact_manager_email": "",
        "platforms": [
            {
                "platform_name": "Facebook",
                "url": "https://www.facebook.com/maitre.olala.officiel",
                "handle": "@maitre.olala.officiel",
                "followers_count": 92000,
                "posts_count": 480,
                "channel_description": "Official communication of iconic defense attorney Maître Olala: human rights defense, courtroom victories, and civic bravery.",
                "engagement_metrics": {
                    "er": "6.7%",
                    "avg_views": "42k"
                }
            }
        ]
    },
    {
        "entity_id": "rija_ramamiarijery",
        "full_name": "Rija Ramamiarijery",
        "alias": "Rija Ramamiarijery (Journalisme d'Investigation)",
        "gender": "Male",
        "residency_status": "Resident",
        "country": "Madagascar",
        "region": "Analamanga",
        "city": "Antananarivo",
        "is_foreign_guest": False,
        "is_humanitarian": False,
        "category_main": "Политика, расследования и гражданский протест",
        "category_sub": "Независимые расследования и диссидентство",
        "tags": "Investigative Journalism, Press Freedom, Corruption Scams, Natural Resources, Media",
        "persona_role": "Независимый журналист-расследователь, продюсер аналитических медиа-материалов, расследующий финансовые махинации и контрабанду ресурсов",
        "content_topics": "Расследования нелегального вывоза сапфиров из Илакаки и золота через частные авиарейсы, схемы хищения топлива в JIRAMA, давление спецслужб на независимую прессу",
        "target_audience": "Читатели расследовательских медиа, международные антикоррупционные институты, журналистское сообщество",
        "primary_language": "Французский",
        "llm_description": "Rija Ramamiarijery is a prominent independent Malagasy investigative journalist. He authors in-depth forensic reports revealing illicit mineral supply chains, public utility procurement fraud, and state security agency intimidation against free journalists in Madagascar.",
        "contact_blogger_phone": "",
        "contact_blogger_email": "rija.ramamiarijery@gmail.com",
        "contact_manager_name": "Rédaction Enquêtes & Vérité",
        "contact_manager_phone": "",
        "contact_manager_email": "",
        "platforms": [
            {
                "platform_name": "Facebook",
                "url": "https://www.facebook.com/rija.ramamiarijery.journaliste",
                "handle": "@rija.ramamiarijery.journaliste",
                "followers_count": 29000,
                "posts_count": 390,
                "channel_description": "Investigative dispatches, anti-corruption inquiries, and documentary journalism on Madagascar.",
                "engagement_metrics": {
                    "er": "5.4%",
                    "avg_views": "16k"
                }
            }
        ]
    },
    {
        "entity_id": "alliance_voahary_gasy",
        "full_name": "Alliance Voahary Gasy",
        "alias": "AVG Madagascar (Vigie des Ressources Naturelles)",
        "gender": "Group",
        "residency_status": "Resident",
        "country": "Madagascar",
        "region": "Analamanga",
        "city": "Antananarivo",
        "is_foreign_guest": False,
        "is_humanitarian": False,
        "category_main": "Политика, расследования и гражданский протест",
        "category_sub": "Независимые расследования и диссидентство",
        "tags": "AVG, Environmental Governance, Rosewood, Whistleblower Hotline, Wildlife Crime, Transparency",
        "persona_role": "Ведущий национальный альянс экологических НКО и гражданских расследователей, оператор зеленой линии 512 для осведомителей об экологических преступлениях",
        "content_topics": "Публичные отчеты о контрабанде розового дерева, эндемичных черепах и лемуров, судебное преследование чиновников-браконьеров, защита прав сельских общин на лесные ресурсы",
        "target_audience": "Экологические организации, международные судебные эксперты, природоохранные активисты, доноры",
        "primary_language": "Французский",
        "llm_description": "Alliance Voahary Gasy (AVG) is Madagascar's premier environmental civil society coalition. Operating a national green whistleblowing hotline (512) and publishing rigorous forensic investigations on natural resource plundering, AVG relentlessly exposes state-sanctioned trafficking syndicates and defends local community conservators.",
        "contact_blogger_phone": "",
        "contact_blogger_email": "contact@alliancevoaharygasy-avg.org",
        "contact_manager_name": "Direction Exécutive AVG",
        "contact_manager_phone": "",
        "contact_manager_email": "coordination.avg@gmail.com",
        "platforms": [
            {
                "platform_name": "Facebook",
                "url": "https://www.facebook.com/alliancevoaharygasy",
                "handle": "@alliancevoaharygasy",
                "followers_count": 49000,
                "posts_count": 780,
                "channel_description": "Official dissemination page of Alliance Voahary Gasy: wildlife crime investigations, forest justice, and civic whistleblowing.",
                "engagement_metrics": {
                    "er": "5.0%",
                    "avg_views": "23k"
                }
            }
        ]
    },
    {
        "entity_id": "sefafi_observatoire_vie_publique",
        "full_name": "SeFaFi",
        "alias": "SeFaFi (Observatoire de la Vie Publique)",
        "gender": "Group",
        "residency_status": "Resident",
        "country": "Madagascar",
        "region": "Analamanga",
        "city": "Antananarivo",
        "is_foreign_guest": False,
        "is_humanitarian": False,
        "category_main": "Политика, расследования и гражданский протест",
        "category_sub": "Независимые расследования и диссидентство",
        "tags": "SeFaFi, Public Policy, Good Governance, Constitutional Watchdog, Civil Society, Democratic Audit",
        "persona_role": "Старейшая и наиболее авторитетная независимая экспертная группа (Observatoire de la Vie Publique), публикующая системный мониторинг государственной политики с 2001 года",
        "content_topics": "Анализ законопроектов, аудит прозрачности выборов, критика авторитарных тенденций, разоблачение деградации системы государственного управления и коммунальных служб",
        "target_audience": "Политические лидеры, дипломатический корпус, ученые-юристы, редакции ведущих изданий, студенты",
        "primary_language": "Французский",
        "llm_description": "SeFaFi (Observatoire de la Vie Publique) is Madagascar's most respected independent public policy watchdog. Operating for over two decades without partisan ties, its intellectual communiqués provide rigorous, uncompromising critiques of executive misconduct, constitutional manipulation, and governance decay.",
        "contact_blogger_phone": "",
        "contact_blogger_email": "sefafi.madagascar@gmail.com",
        "contact_manager_name": "Secrétariat SeFaFi",
        "contact_manager_phone": "",
        "contact_manager_email": "",
        "platforms": [
            {
                "platform_name": "Facebook",
                "url": "https://www.facebook.com/sefafi.madagascar",
                "handle": "@sefafi.madagascar",
                "followers_count": 31000,
                "posts_count": 390,
                "channel_description": "Authoritative civil society watchdog critiques on Madagascar's democracy, rule of law, and public ethics.",
                "engagement_metrics": {
                    "er": "4.7%",
                    "avg_views": "15k"
                }
            }
        ]
    },
    {
        "entity_id": "mouvement_rohy",
        "full_name": "Mouvement ROHY",
        "alias": "Réseau ROHY (Société Civile & Transparence)",
        "gender": "Group",
        "residency_status": "Resident",
        "country": "Madagascar",
        "region": "Analamanga",
        "city": "Antananarivo",
        "is_foreign_guest": False,
        "is_humanitarian": False,
        "category_main": "Политика, расследования и гражданский протест",
        "category_sub": "Независимые расследования и диссидентство",
        "tags": "ROHY, Civil Society Network, Budget Transparency, Good Governance, Citizen Monitoring, Social Accountability",
        "persona_role": "Крупнейшая общенациональная коалиция организаций гражданского общества Мадагаскара (более 100 НКО), эксперты по мониторингу госбюджета и гражданскому контролю",
        "content_topics": "Гражданский аудит государственного бюджета Мадагаскара, мониторинг прозрачности расходов на энергетику и восстановление JIRAMA, защита пространства гражданских свобод",
        "target_audience": "Активисты неправительственного сектора, исследователи публичных финансов, донорские агентства, граждане",
        "primary_language": "Французский",
        "llm_description": "Mouvement ROHY (Réseau des Organisations de la Société Civile pour l'Égalité et la Transparence) is the preeminent civil society umbrella coalition in Madagascar, uniting over 100 grassroots organizations. ROHY leads high-impact citizen budget tracking, monitors utility sector expenditures, and campaigns vigorously against restrictive NGO legislation.",
        "contact_blogger_phone": "",
        "contact_blogger_email": "contact@mouvement-rohy.mg",
        "contact_manager_name": "Coordination Nationale ROHY",
        "contact_manager_phone": "",
        "contact_manager_email": "coordination.rohy@gmail.com",
        "platforms": [
            {
                "platform_name": "Facebook",
                "url": "https://www.facebook.com/mouvement.rohy",
                "handle": "@mouvement.rohy",
                "followers_count": 47000,
                "posts_count": 560,
                "channel_description": "National civil society coalition: citizen budget transparency, public accountability, and fundamental freedoms.",
                "engagement_metrics": {
                    "er": "4.8%",
                    "avg_views": "19k"
                }
            }
        ]
    },
    {
        "entity_id": "kmf_cnoe_fanabeazana",
        "full_name": "KMF/CNOE Fanabeazana Olom-pirenena",
        "alias": "KMF/CNOE (Comité National d'Observation)",
        "gender": "Group",
        "residency_status": "Resident",
        "country": "Madagascar",
        "region": "Analamanga",
        "city": "Antananarivo",
        "is_foreign_guest": False,
        "is_humanitarian": False,
        "category_main": "Политика, расследования и гражданский протест",
        "category_sub": "Независимые расследования и диссидентство",
        "tags": "KMF/CNOE, Election Observation, Civic Education, Democracy, Voter Rights, Election Fraud Monitoring",
        "persona_role": "Национальный комитет наблюдения за выборами и гражданского просвещения (Comité National d'Observation des Élections), старейшая наблюдательная сеть страны",
        "content_topics": "Независимый мониторинг избирательных участков во всех 119 округах Мадагаскара, доклады о подкупе избирателей и фальсификациях протоколов, программы гражданского образования",
        "target_audience": "Избиратели, наблюдатели за выборами, политические партии, международные миссии (ЕС, АС, Франкофония)",
        "primary_language": "Малагасийский",
        "llm_description": "KMF/CNOE Fanabeazana Olom-pirenena is Madagascar's historic national election observation and civic education network. Deploying thousands of volunteer citizen observers across every district during national ballots, KMF/CNOE serves as the ultimate benchmark for electoral integrity and democratic credibility.",
        "contact_blogger_phone": "",
        "contact_blogger_email": "kmfcnoe.madagascar@gmail.com",
        "contact_manager_name": "Bureau Exécutif KMF/CNOE",
        "contact_manager_phone": "",
        "contact_manager_email": "",
        "platforms": [
            {
                "platform_name": "Facebook",
                "url": "https://www.facebook.com/kmfcnoe.madagascar",
                "handle": "@kmfcnoe.madagascar",
                "followers_count": 59000,
                "posts_count": 640,
                "channel_description": "National Election Observation Committee and citizen civic education: protecting universal voting rights.",
                "engagement_metrics": {
                    "er": "5.3%",
                    "avg_views": "25k"
                }
            }
        ]
    },
    {
        "entity_id": "ilontsera_observatoire_medias",
        "full_name": "Ilontsera",
        "alias": "Ilontsera (Observatoire des Médias de Madagascar)",
        "gender": "Group",
        "residency_status": "Resident",
        "country": "Madagascar",
        "region": "Analamanga",
        "city": "Antananarivo",
        "is_foreign_guest": False,
        "is_humanitarian": False,
        "category_main": "Политика, расследования и гражданский протест",
        "category_sub": "Независимые расследования и диссидентство",
        "tags": "Ilontsera, Media Watchdog, Press Freedom, Investigative Journalism, Cybercrime Law Defense",
        "persona_role": "Национальная обсерватория СМИ и коммуникаций Мадагаскара, независимый сторожевой орган свободы печати и прав репортеров",
        "content_topics": "Мониторинг давления властей на редакции независимых радиостанций и газет, противодействие закону о киберпреступности, защита репортеров от судебного преследования",
        "target_audience": "Журналисты, главные редакторы, блогеры, медиаюристы, студенты факультетов журналистики",
        "primary_language": "Французский",
        "llm_description": "Ilontsera (Observatoire des Médias et de la Communication à Madagascar) monitors press freedom violations and media ethics. The organization systematically documents arbitrary arrests of journalists, government broadcasting blackouts, and abusive interpretations of the penal code and cybercrime legislation targeting critical reporters.",
        "contact_blogger_phone": "",
        "contact_blogger_email": "ilontsera.madagascar@gmail.com",
        "contact_manager_name": "Secrétariat Ilontsera",
        "contact_manager_phone": "",
        "contact_manager_email": "",
        "platforms": [
            {
                "platform_name": "Facebook",
                "url": "https://www.facebook.com/ilontsera.observatoire",
                "handle": "@ilontsera.observatoire",
                "followers_count": 21500,
                "posts_count": 320,
                "channel_description": "Media monitoring, press freedom watchdog reports, and investigative journalism training by Ilontsera.",
                "engagement_metrics": {
                    "er": "4.5%",
                    "avg_views": "11k"
                }
            }
        ]
    },
    {
        "entity_id": "me_eric_rafidison",
        "full_name": "Me Eric Rafidison",
        "alias": "Me Eric Rafidison (Avocat Défenseur des Droits Fondamentaux)",
        "gender": "Male",
        "residency_status": "Resident",
        "country": "Madagascar",
        "region": "Analamanga",
        "city": "Antananarivo",
        "is_foreign_guest": False,
        "is_humanitarian": False,
        "category_main": "Политика, расследования и гражданский протест",
        "category_sub": "Независимые расследования и диссидентство",
        "tags": "Human Rights, Barreau, Constitutional Law, Legal Defense, Whistleblower Support, Antananarivo",
        "persona_role": "Адвокат коллегии адвокатов Антананариву, правозащитник, специалист по защите жертв политических репрессий и незаконного изъятия земель",
        "content_topics": "Юридические консультации участникам гражданских протестов, защита информаторов о коррупции, оспаривание незаконных решений министерств в Госсовете",
        "target_audience": "Юристы, правозащитники, гражданские активисты, представители малого бизнеса, пострадавшие от произвола властей",
        "primary_language": "Смешанный",
        "llm_description": "Maître Eric Rafidison is a dedicated human rights lawyer and constitutional jurist practicing at the Antananarivo Bar. He represents civil society whistleblowers, detained student demonstrators, and rural communities resisting uncompensated expropriation, providing a vital legal shield against executive overreach.",
        "contact_blogger_phone": "",
        "contact_blogger_email": "eric.rafidison@barreau-madagascar.org",
        "contact_manager_name": "Cabinet d'Avocat Rafidison",
        "contact_manager_phone": "",
        "contact_manager_email": "",
        "platforms": [
            {
                "platform_name": "Facebook",
                "url": "https://www.facebook.com/me.eric.rafidison",
                "handle": "@me.eric.rafidison",
                "followers_count": 19000,
                "posts_count": 270,
                "channel_description": "Legal counsel, human rights defense briefings, and constitutional reflections by Me Eric Rafidison.",
                "engagement_metrics": {
                    "er": "4.9%",
                    "avg_views": "10k"
                }
            }
        ]
    }
]

# Validation and Aggregation Step
def validate_and_aggregate():
    print(f"Total entities parsed: {len(entities)}")
    assert 40 <= len(entities) <= 55, f"Entity count {len(entities)} out of bounds [40, 55]"

    allowed_categories = {
        "Парламентская оппозиция",
        "Гражданский протест и кризис JIRAMA",
        "Студенческий активизм и профсоюзы",
        "Независимые расследования и диссидентство"
    }

    seen_ids = set()
    for idx, e in enumerate(entities):
        eid = e["entity_id"]
        assert eid not in seen_ids, f"Duplicate entity_id: {eid}"
        seen_ids.add(eid)

        assert e["category_main"] == "Политика, расследования и гражданский протест"
        assert e["category_sub"] in allowed_categories, f"Invalid category_sub: {e['category_sub']} in {eid}"
        assert e["gender"] in ["Male", "Female", "Group"], f"Invalid gender {e['gender']} in {eid}"
        assert e["is_foreign_guest"] is False
        assert e["is_humanitarian"] is False

        # Calculate aggregates
        platforms = e.get("platforms", [])
        assert len(platforms) > 0, f"No platforms for {eid}"

        tot_f = 0
        tot_p = 0
        er_vals = []
        for p in platforms:
            fc = p["followers_count"]
            pc = p["posts_count"]
            assert fc >= 1000, f"Followers < 1000 on {p['platform_name']} for {eid}: {fc}"
            assert pc > 0, f"Posts count <= 0 on {p['platform_name']} for {eid}: {pc}"
            tot_f += fc
            tot_p += pc
            er_str = p["engagement_metrics"]["er"].replace("%", "").strip()
            er_vals.append(float(er_str))

            # URL validation: no bare roots
            url = p["url"]
            assert not re.match(r"^https?://(www\.)?[a-zA-Z0-9\-]+\.[a-z]{2,}/?$", url), f"Bare root URL found: {url} in {eid}"

        e["total_followers_aggregate"] = tot_f
        e["total_posts_aggregate"] = tot_p
        avg_er = sum(er_vals) / len(er_vals)
        e["avg_engagement_rate"] = f"{avg_er:.1f}%"

    output_path = "/Users/n0e1/Downloads/мдг-айти/malagasy_influencers_node_h3_opposition_protest.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(entities, f, indent=2, ensure_ascii=False)

    print(f"Successfully generated and validated {len(entities)} entities.")
    print(f"File saved to: {output_path}")

if __name__ == "__main__":
    validate_and_aggregate()
