Postup:

1. Vytvoření složky Ukol_03 a podslozek data, data_transformer
2. Pres AI vytvoreni smyleneho datasetu v csv a ulozeni do slozky data
3. Vytvoření demo databaze mongo pres powershell prikazem docker run --rm -p 27017:27017 --name "mongoDB" mongo:latest
3. Vytvoreni souboru mongo_basic.py se zakladnimi operacemi pro mongo DB (Transformacni script pouziva jen jednu, ale chtel jsem si to zkusit)
4. Vytvoreni souboru data_transform.py, ktery taha data z csv souboru a transformuje je do formatu pro mongo a to ve frontach po 25 radcich, mezi kterymi je 30s pauza, ktera jako simuluje nacitani dat v realnem case. 
5. Spolecne ladeni a testovani obou python souboru data_transform a mongo_basic
6. Usporadani podslozek ve slozce Ukol_03
8. Zruseni testovaci mongo db
8. Vytvoreni souboru http_server.py, ktery ma jen metodu GET, která umoznuje filtrovat dotazy.
9. Testovani http serveru pres prikazy z powershell.
10. Vytvoreni obou souboru dockerfile a souboru requirements.txt
11. Vytvoreni docker-compose.yaml
12. Prepnuti se do prislusneho adresare v powershellu a vytvoreni potrebnych image, docker site a docker kontejneru tak jak je specifikovano v souboru docker-compse.yml a to prikazem v powershell docker-compose up --build
13. Ziskani response pres powershell z http-serveru napr prikazem  curl http://localhost:8000/machine_data?status=IDLE

Samozrejme jsem si pomahal AI. Ja se proste vsechno ucim a mam jen malou praxi co se programovani tyce, ale zajima mě to a chci se ucit. Vzdy kdyz se neco ucim, tak se snazim to aplikovat pro svoje vyuzití, protoze tak si nejlepe ponorim do tematu, kdyz vim co chci vytvorit. Kdyz mam jasnou hmatatelnou predstavu a vim jaky mam byt vystup, tak je to vzdy snazi. Coz v tomto pripade tak nebylo, ne vsechno pro mě bylo uchopitelne, a v praxi pouzitelne, ale i tak byl cely kurz Velikou inspiraci a rozsireni si vlastnich obzoru.
Ja vím, ze to neni ani zdaleka perfektni, ze chyby komentare a dockstringy apod., na ktere uz jsem proste nemel cas a silu: -) (V praci si je zamozrejme delam) ,ale myslim si, ze podstatu, zejmena prace s Dockerem jsem pochopil. Snad za to i tak a pres spozdeni nejake body budou.

Planuji si cely kurz pekne v klidu a vlastnim tempem projit a veci si poradne zazit, protoze je doslova nabitej informacema a pro mě neskutecnejma moznostma.  

Diky