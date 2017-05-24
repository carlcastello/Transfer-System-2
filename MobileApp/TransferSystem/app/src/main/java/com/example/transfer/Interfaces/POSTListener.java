package com.example.transfer.Interfaces;

import org.json.JSONObject;

/**
 * Created by carlcastello on 23/05/17.
 */

public interface POSTListener {
    public abstract void userAuthenticated(JSONObject jsonObject);
    public abstract void revertActivity();
}
