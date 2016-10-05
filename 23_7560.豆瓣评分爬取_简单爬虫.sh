#!/bin/bash

for((i=0;i<170;i=i+25));
do 
if [[ "$i" -lt 150 ]]; then        
    echo $(curl "https://movie.douban.com/top250?start="$i | grep v:average | grep -o [0-9]\.[0-9] | awk '{total+=$1}END{print total}');
else        
    echo $(curl "https://movie.douban.com/top250?start="$i | grep v:average | head -16 | grep -o [0-9]\.[0-9] | awk '{total+=$1}END{print total}')    
fi
done | awk '{total+=$1}END{print total}'
# 前面的 awk 的输出都传到了最后这里, 最后只有一个输出
# grep -o 只输出匹配的文字

# 刚爬完, 豆瓣就不让爬了...
