# EDIC_Calculate
![](https://user-images.githubusercontent.com/4284040/50399950-0aed1100-07be-11e9-82eb-584b910ee8b9.PNG "數學公式")
* 將 `測試資料` 輸入後，更改 `使用者定義函數` 或 `系統預設涵式` ，將可取得相對 x-y axis 圖形
Example :
* input : `'*.csv,'`, ~~`'*.txt'`~~, ~~`'*.xlxs'`~~, ~~`'*.xls'`~~
* ouput : `''`

# Getting Started
## 系統需求
* `Python 3.0+`, `Git 2.0+`
>若要使用 `Visual Studio code` 執行，需要裝 `Python`, `Code Runner`。
>>[補充] `Visual Studio code` 中安裝 `Markdown Preview Github Styling`, `Auto-Open Markdown Preview` 可編輯 `ReadMe.md` 並即時顯示

## 安裝套件
若第一次執行程式，請打開 `CMD` 或 `Powershell` 執行以下安裝指令
```
pip install configparser numpy matplotlib pillow --upgrade pip
```

## 設定檔
建立設定檔 config.ini 放置於專案根目錄下
* config.ini 內容如下 :
>[`parameter`]
```
tfe=(tFE)→100x10e-7
ec=(Ec)→1x10E6
pr=(Pr)→9x10E-6
f_len=(浮點數運算取長度)→50
```
>[`file`]
```
src=(原測試資料目錄)→預設空
dst=(生成後資料目錄)→預設空
src_f_org=(原測試資料 V, Q)→omap.csv
src_f_map=(原參照資料 V, I)→mmap.csv
dst_f_new=(生成資料部分)→nmap.csv
dst_f_all=(生成資料全)→amap.csv
```
>[`graphic`]
```
g_fmt=(生成圖片格式)→svg
g_title=(圖形名稱)→png
g_name=(生成圖片名稱)→V-I graphic
g_x_axis=(x軸名稱)→voltage (V.)
g_y_axis=(y軸名稱)→current (I.)
```

## 程式執行
切入程式放置資料夾，同時點選 `滑鼠右鍵` 和 `鍵盤Shift`，點擊 `在這裡開啟 Powershell 視窗` 或 `在這裡開啟 CMD 視窗`，在 `Powershell` 或 `CMD` 輸入下列程式命令
```
python main.py
```

## 後續補充
待續......

