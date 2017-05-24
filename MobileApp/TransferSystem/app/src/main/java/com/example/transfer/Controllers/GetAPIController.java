package com.example.transfer.Controllers;

import android.content.Context;
import android.os.AsyncTask;
import android.widget.Toast;

import com.example.transfer.Interfaces.GETListener;
import com.example.transfer.Interfaces.POSTListener;

import org.apache.commons.io.IOUtils;
import org.json.JSONObject;

import java.io.BufferedInputStream;
import java.io.InputStream;
import java.net.HttpURLConnection;
import java.net.URL;

/**
 * Created by carlcastello on 23/05/17.
 */

// https://code.tutsplus.com/tutorials/android-from-scratch-using-rest-apis--cms-27117
public class GetAPIController {
    public static class ArticleTask extends AsyncTask<JSONObject, Void, String> {
        final private String url = "http://10.0.2.2:8000/app/api/";
        private Context ContextAsync;

        public ArticleTask(Context context) {
            this.ContextAsync = context;
        }

        @Override
        protected void onPreExecute() {
            super.onPreExecute();
        }

        @Override
        protected String doInBackground(JSONObject... jsonObjects) {
            HttpURLConnection client = null;
            JSONObject jsonObject = jsonObjects[0];
            try {
                String token = jsonObject.getString("token");
                String id = jsonObject.getString("id");

                URL url = new URL(this.url+id);
                client = (HttpURLConnection) url.openConnection();


                client.setRequestMethod("GET");
                client.setRequestProperty("Content-Type", "application/json");
                client.setRequestProperty("accept","application/json");
                client.setRequestProperty("accept-encoding", "gzip, deflate");
                client.setRequestProperty("accept-language", "en-US,en;q=0.8");
                client.setRequestProperty("Authorization","JWT "+ token);
                client.setDoInput(true);

                InputStream inputStream = new BufferedInputStream(client.getInputStream());
                String result = IOUtils.toString(inputStream, "UTF-8");
                inputStream.close();

                return result;
            } catch (Exception error) {
                System.out.println(error);
                return null;
            }
        }

        @Override
        protected void onPostExecute(String result) {
            if (result != null) {
                JSONObject articleJson = null;
                try {
                    articleJson = new JSONObject(result);
                } catch (Exception error) {
                    System.out.println(error);
                }
                GETListener getListener = (GETListener) ContextAsync;
                getListener.articleExtraction(articleJson);
            } else {
                Toast.makeText(ContextAsync,"Invalid Article Number",Toast.LENGTH_LONG).show();
            }
        }
    }
}
