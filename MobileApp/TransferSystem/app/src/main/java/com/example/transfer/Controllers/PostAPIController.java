package com.example.transfer.Controllers;

import android.content.Context;
import android.os.AsyncTask;
import android.widget.Toast;

import com.example.transfer.Interfaces.POSTListener;

import org.apache.commons.io.IOUtils;
import org.json.JSONObject;

import java.io.BufferedInputStream;
import java.io.BufferedOutputStream;
import java.io.InputStream;
import java.io.OutputStream;
import java.net.HttpURLConnection;
import java.net.URL;

/**
 * Created by carlcastello on 23/05/17.
 */

// https://code.tutsplus.com/tutorials/android-from-scratch-using-rest-apis--cms-27117
public class PostAPIController {
    public static class AuthenticateTask extends AsyncTask<JSONObject, Void, String> {
        final private String url = "http://10.0.2.2:8000/api/login/";
        private Context ContextAsync;

        public AuthenticateTask(Context context) {
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
                URL url = new URL(this.url);
                client = (HttpURLConnection) url.openConnection();

                client.setRequestMethod("POST");
                client.setRequestProperty("undefinedaccept", "application/json");
                client.setRequestProperty("accept-encoding", "gzip, deflate");
                client.setRequestProperty("accept-language", "en-US,en;q=0.8");
                client.setRequestProperty("content-type", "application/json");
                client.setDoOutput(true);

                JSONObject userInfo = new JSONObject();
                userInfo.put("username", jsonObject.get("username"));
                userInfo.put("password", jsonObject.get("password"));
                String input = userInfo.toString();

                OutputStream outputStream = new BufferedOutputStream(client.getOutputStream());
                outputStream.write(input.getBytes());
                outputStream.flush();
                outputStream.close();

                InputStream inputStream = new BufferedInputStream(client.getInputStream());
                String result = IOUtils.toString(inputStream, "UTF-8");
                inputStream.close();
                return result;
            } catch (Exception error) {
                return null;
            }
        }

        @Override
        protected void onPostExecute(String result) {
            if (result != null) {
                JSONObject userJson = null;
                try {
                    userJson = new JSONObject(result);
                } catch (Exception error) {
                    System.out.println(error);
                }
                POSTListener POSTListener = (POSTListener) ContextAsync;
                POSTListener.userAuthenticated(userJson);
            } else {
                Toast.makeText(ContextAsync,"Invalid User Credentials",Toast.LENGTH_LONG).show();
            }
        }
    }

    public static class TransferTask extends AsyncTask<JSONObject, Void, Boolean> {
        final private String url = "http://10.0.2.2:8000/app/api/";
        private Context ContextAsync;

        public TransferTask(Context context) {
            this.ContextAsync = context;
        }

        @Override
        protected void onPreExecute() {
            super.onPreExecute();
        }

        @Override
        protected Boolean doInBackground(JSONObject... jsonObjects) {
            HttpURLConnection client = null;
            JSONObject jsonObject = jsonObjects[0];
            try {
                URL url = new URL(this.url + jsonObject.get("id"));
                client = (HttpURLConnection) url.openConnection();

                client.setRequestMethod("POST");
                client.setRequestProperty("Content-Type", "application/json");
                client.setRequestProperty("accept","application/json");
                client.setRequestProperty("accept-encoding", "gzip, deflate");
                client.setRequestProperty("accept-language", "en-US,en;q=0.8");
                client.setRequestProperty("Authorization","JWT "+ jsonObject.get("token"));
                client.setDoOutput(true);


                JSONObject userInfo = new JSONObject();
                userInfo.put("location", jsonObject.get("location"));
                userInfo.put("quantity", jsonObject.get("quantity"));
                String input = userInfo.toString();

                OutputStream outputStream = new BufferedOutputStream(client.getOutputStream());
                outputStream.write(input.getBytes());
                outputStream.flush();
                outputStream.close();

                InputStream inputStream = new BufferedInputStream(client.getInputStream());
                String result = IOUtils.toString(inputStream, "UTF-8");
                inputStream.close();
                System.out.println(result);



                return true;
            } catch (Exception error) {
                System.out.println(error);
                return false;
            }
        }

        @Override
        protected void onPostExecute(Boolean result) {
            if (result) {
                POSTListener POSTListener = (POSTListener) ContextAsync;
                POSTListener.revertActivity();
            } else {
                Toast.makeText(ContextAsync,"Something went wrong",Toast.LENGTH_LONG).show();
            }
        }
    }
}
