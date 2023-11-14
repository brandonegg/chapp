start_client() {
  echo "I'm client"
}

start_server() {
  echo "I'm server"
}

case $1 in
  client)
    start_client
  ;;

  server)
    start_server
  ;;

  **)
    echo "Invalid option $1 - valid subcommand = {client|server}"
  ;;
esac