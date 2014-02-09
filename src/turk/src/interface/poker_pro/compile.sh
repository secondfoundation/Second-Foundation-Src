mkdir build
javac -cp thirdparty/meerkat-api.jar:thirdparty/smtp.jar:thirdparty/activation.jar:thirdparty/mailapi.jar -d build -sourcepath src src/ca/ualberta/cs/poker/free/client/*.java src/ca/ualberta/cs/poker/free/alien/*.java src/ca/ualberta/cs/poker/free/server/*.java src/ca/ualberta/cs/poker/free/dynamics/*.java src/ca/ualberta/cs/poker/free/academy25/*.java src/ca/ualberta/cs/poker/free/tournament/*.java src/*.java
jar cf aaaibot.jar -C build ca -C build StreamConnect.class -C build TCPPlugin.class
