start_client() {
  python3 -m chat_app.client
}

start_server() {
  python3 -m chat_app.server
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