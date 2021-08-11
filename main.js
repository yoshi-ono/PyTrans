function doGet(e) {
  var text = e.parameter.text;
  return ContentService.createTextOutput("text is " + text);
}

function doPost(e) {
    Logger.log(e);  // GCP でログが見れるらしい（Cloud のログ）
    
    // リクエストパラメータを取得する
    var p = e.parameter;
    // LanguageAppクラスを用いて翻訳を実行
    var translatedText = LanguageApp.translate(p.text, p.source, p.target);
    // var translatedText = LanguageApp.translate("a", "en", "ja");
    // レスポンスボディの作成
    var body;
    if (translatedText) {
        body = {
          code: 200,
          text: translatedText,
          e: e
        };
    } else {
        body = {
          code: 400,
          text: "Bad Request",
          e: e
        };
    }
    // レスポンスの作成
    var response = ContentService.createTextOutput();
    // Mime TypeをJSONに設定
    response.setMimeType(ContentService.MimeType.JSON);
    // JSONテキストをセットする
    response.setContent(JSON.stringify(body));

    return response;
}
