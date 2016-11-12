from bson import Code
from pymongo import MongoClient

client = MongoClient()
db = client.music_db
price = "1"
map = Code("db.album.mapReduce( "
                   "                    function(){"
                   "    for(var i=0 in this.songs){"
                   "        if(this.songs[i].price>"+price+"){"
                   "            emit(this.songs[i].price, 1);"
                   "            }"
                   "        }"
                   "    }")
reduce = Code("function(key, values){"
                   "    var sum = 0;"
                   "    for( var i=0 in values){"
                   "        sum+=values[i];"
                   "        }"
                   "    return sum;"
                   "    }")
db.album.map_reduce(map, reduce, "myresult")