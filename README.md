# Watson API を呼び出すアプリをIBM Kubernetes上で動かそう with Python Flask
Python Flask上からWatson Visual Recognitionwith APIを呼び出して画像認識結果を戻すアプリケーションのサンプルです。

IBM Kubernetes Service上で動かす方法は以下を参照ください:
https://speakerdeck.com/kyokonishito/iks-watson-vr-flask
(顔検出はVisual Recognitionから削除されたため、ソースから削除しました。上記改訂版は2016/09/09にUp予定)

IBM Kubernetes Service以外のコンテナ環境で動作させる場合：
 - ibm-credentials.env.sampleを参考にしてAPI KEYとURLをセットして作成するか、IBM Cloud上のVisual RecongnitionのWeb管理ページからダウンロードしてibm-credentials.envをルートにおいてください。


ローカル環境で動作させる場合は上記の設定に加えて以下を設定してください：  
 - 環境変数 `IBM_CREDENTIALS_FILE` に ibm-credentials.envをフルパスで設定してください。

