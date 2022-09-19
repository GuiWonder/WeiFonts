#!/bin/sh
#Replace Windows Chinese Fonts
mkdir -p AA
wget -nc -P AA https://github.com/GuiWonder/SourceHanToClassic/releases/download/test-ttf-0001/AdvocateAncientSansTTFs.7z
#wget -nc -P AA https://github.com/GuiWonder/SourceHanToClassic/releases/download/1.005/AdvocateAncientSerifSC.7z
7z e ./AA/AdvocateAncientSansTTFs.7z -o./AA
#7z e ./AA/AdvocateAncientSerifSC.7z -o./AA
chmod +x ./main/otfcc/*
mkdir -p out
python3 ./main/winfont.py ./AA/AdvocateAncientSansSC/AdvocateAncientSansSC-Regular.ttf
python3 ./main/winfont.py ./AA/AdvocateAncientSansSC/AdvocateAncientSansSC-Bold.ttf
python3 ./main/winfont.py ./AA/AdvocateAncientSansSC/AdvocateAncientSansSC-Light.ttf
7z a ./out/msyh.7z ./msyh*.ttc
python3 ./main/winfont.py ./AA/AdvocateAncientSansTC/AdvocateAncientSansTC-Regular.ttf
python3 ./main/winfont.py ./AA/AdvocateAncientSansTC/AdvocateAncientSansTC-Bold.ttf
python3 ./main/winfont.py ./AA/AdvocateAncientSansTC/AdvocateAncientSansTC-Light.ttf
7z a ./out/msjh.7z ./msjh*.ttc
#7z a ./out/simsun.7z ./simsun.ttc
rm -rf ./AA
rm -f ./*.otf
rm -f ./*.ttf
rm -f ./*.ttc
