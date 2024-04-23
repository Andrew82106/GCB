# gitUpdate.sh脚本，用于简化git的提交操作，包括添加、提交和推送。
# 添加一个变量，用于存储提交信息，这个信息通过输入得到
echo "请输入提交信息："
read commit_message
git add .
# 使用提交信息中的变量
git commit -m "$commit_message"
git push origin master:Andrew82106