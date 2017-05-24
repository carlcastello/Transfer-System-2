package com.example.transfer.Controllers;

import android.content.Context;

import com.example.transfer.Models.User;

import org.json.JSONObject;

/**
 * Created by carlcastello on 23/05/17.
 */

public class ArticleController {
    private JSONObject data;
    private Context context;

    public ArticleController(Context context, String articleNumber, User user) {
        this.data = new JSONObject();
        try {
            this.data.put("id",articleNumber);
            this.data.put("token",user.getToken());
        } catch (Exception error) {
            System.out.println(error);
        }
        this.context = context;
    }

    public void get(){

        GetAPIController.ArticleTask getAPIController = new GetAPIController.ArticleTask(this.context);
        getAPIController.execute(this.data);
    }
}
