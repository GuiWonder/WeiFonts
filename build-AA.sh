#!/bin/sh
#Replace Windows Chinese Fonts
mkdir -p AA
wget -nc -P AA https://github.com/GuiWonder/SourceHanToClassic/releases/download/1.005/AdvocateAncientSansSC.7z
wget -nc -P AA https://github.com/GuiWonder/SourceHanToClassic/releases/download/1.005/AdvocateAncientSerifSC.7z
7z e ./AA/AdvocateAncientSansSC.7z -o./AA
7z e ./AA/AdvocateAncientSerifSC.7z -o./AA
chmod +x ./main/otfcc/*
python3 ./main/winfont.py ./AA/AdvocateAncientSansSC-Regular.otf
python3 ./main/winfont.py ./AA/AdvocateAncientSansSC-Bold.otf
python3 ./main/winfont.py ./AA/AdvocateAncientSansSC-Light.otf
python3 ./main/winfont.py ./AA/AdvocateAncientSansSC-ExtraLight.otf
python3 ./main/winfont.py ./AA/AdvocateAncientSansSC-Heavy.otf
python3 ./main/winfont.py ./AA/AdvocateAncientSerifSC-Regular.otf
mkdir -p out
7z a ./out/msyh.7z ./msyh*.ttc
7z a ./out/msjh.7z ./msjh*.ttc
7z a ./out/simsun.7z ./simsun.ttc
rm -rf ./AA
rm -f ./*.otf
rm -f ./*.ttf
rm -f ./*.ttc
