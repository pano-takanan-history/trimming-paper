download:
	cd cldf-datasets; git clone https://github.com/sequencecomparison/hattorijaponic
	cd cldf-datasets; git clone https://github.com/sequencecomparison/houchinese
	cd cldf-datasets; git clone https://github.com/SequenceComparison/zhivlovobugrian
	cd cldf-datasets; git clone https://github.com/lexibank/constenlachibchan
	cd cldf-datasets; git clone https://github.com/lexibank/crossandean
	cd cldf-datasets; git clone https://github.com/lexibank/dravlex
	cd cldf-datasets; git clone https://github.com/lexibank/felekesemitic
	cd cldf-datasets; git clone https://github.com/lexibank/leekoreanic
	cd cldf-datasets; git clone https://github.com/lexibank/robinsonap
	cd cldf-datasets; git clone https://github.com/lexibank/walworthpolynesian

preprocessing:
	edictor wordlist --dataset=cldf-datasets/hattorijaponic/cldf/cldf-metadata.json --name=datasets/hattorijaponic --preprocessing=edictor/base.py --addon="cogid_cognateset_id:cog"
	edictor wordlist --dataset=cldf-datasets/houchinese/cldf/cldf-metadata.json --name=datasets/houchinese --preprocessing=edictor/base.py --addon="cogid_cognateset_id:cog"
	edictor wordlist --dataset=cldf-datasets/zhivlovobugrian/cldf/cldf-metadata.json --name=datasets/zhivlovobugrian --preprocessing=edictor/base.py --addon="cogid_cognateset_id:cog"
	edictor wordlist --dataset=cldf-datasets/constenlachibchan/cldf/cldf-metadata.json --name=datasets/constenlachibchan --preprocessing=edictor/base.py --addon="cogid_cognateset_id:cog"
	edictor wordlist --dataset=cldf-datasets/crossandean/cldf/cldf-metadata.json --name=datasets/crossandean --preprocessing=edictor/crossandean.py --addon="cogid_cognateset_id:cogid"
	edictor wordlist --dataset=cldf-datasets/dravlex/cldf/cldf-metadata.json --name=datasets/dravlex --preprocessing=edictor/base.py --addon="cogid_cognateset_id:cog"
	edictor wordlist --dataset=cldf-datasets/felekesemitic/cldf/cldf-metadata.json --name=datasets/felekesemitic --preprocessing=edictor/base.py --addon="cogid_cognateset_id:cog"
	edictor wordlist --dataset=cldf-datasets/leekoreanic/cldf/cldf-metadata.json --name=datasets/leekoreanic --preprocessing=edictor/base.py --addon="cogid_cognateset_id:cog"
	edictor wordlist --dataset=cldf-datasets/robinsonap/cldf/cldf-metadata.json --name=datasets/robinsonap --preprocessing=edictor/base.py --addon="cogid_cognateset_id:cog"
	edictor wordlist --dataset=cldf-datasets/walworthpolynesian/cldf/cldf-metadata.json --name=datasets/walworthpolynesian --preprocessing=edictor/reduce_varieties.py --addon="cogid_cognateset_id:cogid"
preprocessing-library:
	edictor wordlist --dataset=cldf-datasets/crossandean/cldf/cldf-metadata.json --name=datasets/crossandean_lib --preprocessing=edictor/crossandean-library.py --addon="cogid_cognateset_id:cogid"
	edictor wordlist --dataset=cldf-datasets/leekoreanic/cldf/cldf-metadata.json --name=datasets/leekoreanic_lib --preprocessing=edictor/base-library.py --addon="cogid_cognateset_id:cog"
	edictor wordlist --dataset=cldf-datasets/felekesemitic/cldf/cldf-metadata.json --name=datasets/felekesemitic_lib --preprocessing=edictor/base-library.py --addon="cogid_cognateset_id:cog"
	edictor wordlist --dataset=cldf-datasets/sidwellvietic/cldf/cldf-metadata.json --name=datasets/sidwellvietic_lib --preprocessing=edictor/base-library.py --addon="cogid_cognateset_id:cog"
	edictor wordlist --dataset=cldf-datasets/hattorijaponic/cldf/cldf-metadata.json --name=datasets/hattorijaponic_lib --preprocessing=edictor/base-library.py --addon="cogid_cognateset_id:cog"
	edictor wordlist --dataset=cldf-datasets/houchinese/cldf/cldf-metadata.json --name=datasets/houchinese_lib --preprocessing=edictor/base-library.py --addon="cogid_cognateset_id:cog"

measure:
	python trim.py
