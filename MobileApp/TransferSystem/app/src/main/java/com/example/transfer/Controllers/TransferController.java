package com.example.transfer.Controllers;


import android.content.Context;

import com.example.transfer.Activities.ProcessTransferActivity;
import com.example.transfer.Models.Article;
import com.example.transfer.Models.User;

import org.json.JSONObject;

/**
 * Created by carlcastello on 23/05/17.
 */

public class TransferController {
    private JSONObject data;
    private Context context;

    public TransferController(Context context, Article article, String location, int quantity, User user) {
        this.data = new JSONObject();
        try {
            this.data.put("id",article.getId());
            this.data.put("location",location);
            this.data.put("quantity",quantity);
            this.data.put("token",user.getToken());
        } catch (Exception error) {
            System.out.println(error);
        }
        this.context = context;
    }

    public void post() {
        PostAPIController.TransferTask tt = new PostAPIController.TransferTask(this.context);
        tt.execute(data);
    }
}
