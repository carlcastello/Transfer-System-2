package com.example.transfer.Activities;

import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.EditText;

import com.example.transfer.Controllers.LogInController;
import com.example.transfer.Interfaces.POSTListener;
import com.example.transfer.Models.User;
import com.example.transfer.R;

import org.json.JSONObject;

public class MainActivity extends AppCompatActivity implements POSTListener {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
    }

    /** Called when the user clicks the singIn button */
    public void signInButton(View view) {
        String username = ((EditText) findViewById(R.id.user_name_input)).getText().toString();
        String password = ((EditText) findViewById(R.id.user_password_input)).getText().toString();

        LogInController logInController = new LogInController(this,username,password);
        logInController.post();
    }

    @Override
    public void userAuthenticated(JSONObject userJson) {
        User user = new User(userJson);
        Intent intent = new Intent(this, ReadNumberActivity.class);
        intent.putExtra("User", user);
        startActivity(intent);
    }

    @Override
    public void revertActivity(){};
}
