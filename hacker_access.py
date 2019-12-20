import json
import requests


def get_user_posts(username, filter_posts="all", limit=100):
    """
    Filter by type of item. 
    One of "job", "story", "comment", "poll", or "pollopt"
    Default: type='comment', limit='100'
    """
    # TODO: currently only supports 'comment' type

    response = requests.get(f'https://hacker-news.firebaseio.com/v0/user/{username}.json')
    post_ids = response.json()["submitted"]
    
    filtered_post_ids = []
    filtered_posts = []
   
    for post_id in post_ids:
        
        # post is a python dict
        post = requests.get(f'https://hacker-news.firebaseio.com/v0/item/{post_id}.json').json()

        if (post['type'] == filter_posts):
            
            text = post.get('text')   
            
            # text==null if post was deleted
            if text:
                filtered_posts.append(text)
                filtered_post_ids.append(post_id)
        
        # Checks whether the specified limit has been reached
        if len(filtered_posts) == limit:
            break

    return filtered_post_ids, filtered_posts

def get_user_list(criteria='top100'):
    if criteria=='top100':
        users_string = '''tptacek	sd
                        2.	jacquesm	sd
                        3.	patio11	sd
                        4.	danso	sd
                        5.	ingve	sd
                        6.	ColinWright	sd
                        7.	rayiner	sd
                        8.	ChuckMcM	sd
                        9.	rbanffy	sd
                        10.	prostoalex11.	sd
                        11. Animats	79907
                        12.	mikeash	74346
                        13.	edw519	73178
                        14.	jgrahamc	71990
                        15.	JumpCrisscross	71683
                        16.	dragonwriter	68034
                        17.	TeMPOraL	67554
                        18.	steveklabnik	67203
                        19.	uptown	66695
                        20.	shawndumas	66398
                        21.	nostrademons	63728
                        22.	luu	63128
                        23.	jerf	62527
                        24.	anigbrowl	61255
                        25.	coldtea	60694
                        26.	llambda	58088
                        27.	fogus	56893
                        28.	Tomte	55753
                        29.	jrockway	54930
                        30.	jseliger	54593
                        31.	pjc50	53735
                        32.	aaronbrethorst	53634
                        33.	cperciva	52499
                        34.	adamnemecek	52486
                        35.	davidw	52403
                        36.	pseudolus	52078
                        37.	DanBC	51403
                        38.	lelf	51133
                        39.	dnetesn	50649
                        40.	tosh	50647
                        41.	pjmlp	50620
                        42.	jonbaer	50451
                        43.	smacktoward	49551
                        44.	icebraining	47671
                        45.	coloneltcb	47628
                        46.	bane	46130
                        47.	wallflower	45600
                        48.	evo_9	45514
                        49.	nkurz	45305
                        50.	robin_reala	44759
                        51.	sp332	44413
                        52.	protomyth	43336
                        53.	wglb	43152
                        54.	walterbell	42181
                        55.	DanielBMarkham	42018
                        56.	untog	41473
                        57.	masklinn	41465
                        58.	userbinator	41398
                        59.	DiabloD3	40939
                        60.	petercooper	40624
                        61.	minimaxir	40221
                        62.	StavrosK	40031
                        63.	_delirium	39962
                        64.	signa11	39552
                        65.	btilly	39454
                        66.	zdw	38199
                        67.	grellas	37716
                        68.	bpierre	37253
                        69.	pavel_lishin	37120
                        70.	lisper	36755
                        71.	rdl	36589
                        72.	sethbannon	36380
                        73.	pcwalton	36356
                        74.	rdtsc	36352
                        75.	brudgers	35987
                        76.	stcredzero	35499
                        77.	toomuchtodo	35499
                        78.	pmoriarty	35443
                        79.	mpweiher	34665
                        80.	derefr	34356
                        81.	JoshTriplett	34267
                        82.	noonespecial	33911
                        83.	adventured	33881
                        84.	Garbage	33417
                        85.	jedberg	33101
                        86.	Retric	33100
                        87.	mtgx	33090
                        88.	sohkamyung	32766
                        89.	SwellJoe	32631
                        90.	Anon84	32493
                        91.	jonknee	32481
                        92.	cpeterso	32282
                        93.	wpietri	31987
                        94.	Someone1234	31715
                        95.	dredmorbius	31604
                        96.	scott_s	31496
                        97.	ilamont	30390
                        98.	nostromo	30147
                        99.	gruseom	30044
                        100.	philwelch	30032
                        '''
        # Debug code
        input_list = users_string.split()
        user_list = []
        # Generates indices from 0 on in intervals of 3
        user_indices = list(range(100))[0::3]
        for i in user_indices:
            user_list.append(input_list[i])
        
        return user_list