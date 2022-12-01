#!/bin/sh
#Replace Windows Chinese Fonts
#mkdir -p ./out
mkdir -p AA
wget -nc -P AA https://github.com/GuiWonder/SourceHanToClassic/releases/download/1.010-ttf/AdvocateAncientSansTTFs.7z
7z e ./AA/AdvocateAncientSansTTFs.7z -o./AA -aoa
chmod +x ./main/otfcc/*
mkdir -p ./yh
mkdir -p ./yhui
mkdir -p ./jh
mkdir -p ./jhui

python3 ./main/winfont.py ./AA/AdvocateAncientSansSC-Regular.ttf
python3 ./main/winfont.py ./AA/AdvocateAncientSansSC-Bold.ttf
python3 ./main/winfont.py ./AA/AdvocateAncientSansSC-Light.ttf
mv *.tt* ./yh/
mv *.otf ./yh/
python3 ./main/winfont.py ./AA/AdvocateAncientSansHWSC-Regular.ttf
python3 ./main/winfont.py ./AA/AdvocateAncientSansHWSC-Bold.ttf
python3 ./main/winfont.py ./AA/AdvocateAncientSansHWSC-Light.ttf
mv *.tt* ./yhui/
mv *.otf ./yhui/
python3 ./main/winfont.py ./AA/AdvocateAncientSansTC-Regular.ttf
python3 ./main/winfont.py ./AA/AdvocateAncientSansTC-Bold.ttf
python3 ./main/winfont.py ./AA/AdvocateAncientSansTC-Light.ttf
mv *.tt* ./jh/
mv *.otf ./jh/
python3 ./main/winfont.py ./AA/AdvocateAncientSansHWTC-Regular.ttf
python3 ./main/winfont.py ./AA/AdvocateAncientSansHWTC-Bold.ttf
python3 ./main/winfont.py ./AA/AdvocateAncientSansHWTC-Light.ttf
mv *.tt* ./jhui/
mv *.otf ./jhui/
python3 ./main/otf2otc.py -o ./msyh.ttc ./yh/msyh.otf ./yhui/msyhui.otf
python3 ./main/otf2otc.py -o ./msyhbd.ttc ./yh/msyhbd.otf ./yhui/msyhbdui.otf
python3 ./main/otf2otc.py -o ./msyhl.ttc ./yh/msyhl.otf ./yhui/msyhlui.otf
python3 ./main/otf2otc.py -o ./msjh.ttc ./jh/msjh.otf ./jhui/msjhui.otf
python3 ./main/otf2otc.py -o ./msjhbd.ttc ./jh/msjhbd.otf ./jhui/msjhbdui.otf
python3 ./main/otf2otc.py -o ./msjhl.ttc ./jh/msjhl.otf ./jhui/msjhlui.otf

7z a ./msyh.7z ./msyh*.ttc
7z a ./msjh.7z ./msjh*.ttc
