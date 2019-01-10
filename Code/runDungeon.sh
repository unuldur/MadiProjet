for file in ../Dungeons/*
do
  echo $file
#  python3 main.py -r 15
  python3 main.py -d  $file --pdmGurobi -s 10
done
