package com.example.transfer.Controllers;

import android.content.Context;

import org.json.JSONObject;

/**
 * Created by carlcastello on 23/05/17.
 */

public class LogInController {
    private JSONObject userInfo;
    private Context context;

    public LogInController(Context context, String username, String password) {
        this.userInfo = new JSONObject();
        try {
            this.userInfo.put("username",username);
            this.userInfo.put("password",password);
        } catch (Exception error) {
            System.out.println(error);
        }
        this.context = context;
    }

    public void post() {
        PostAPIController.AuthenticateTask LoginAuthenticate = new PostAPIController.AuthenticateTask(this.context);
        LoginAuthenticate.execute(this.userInfo);
    }

}
