package com.example.transfer.Models;

import org.json.JSONObject;
import java.io.Serializable;

/**
 * Created by carlcastello on 23/05/17.
 */

public class User implements Serializable {
    // http://hmkcode.com/android-passing-java-object-another-activity/
    private static final long serialVersionUID = 1L;

    private String username;
    private String token;

    public User(JSONObject userInfo) {
        try {
            JSONObject user = userInfo.getJSONObject("user");
            this.username = user.getString("username");
            this.token = userInfo.getString("token");

        } catch (Exception error) {
            System.out.println(error);
        }
    }

    public String getUsername() {
        return username;
    }

    public String getToken() {
        return token;
    }

    public String toString() {
        return "User [ username=" + this.username + ", token=" + this.token + "]";
    }
}
