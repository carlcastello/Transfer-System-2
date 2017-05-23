package com.example.transfer;

import android.content.Intent;
import android.support.v7.app.AlertDialog;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;

public class ReadNumberActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_read_number);
    }

    /** Called when the user clicks the singOut button */
    public void signOutButton(View view) {
        Intent intent = new Intent(this, MainActivity.class);
        // Deletes previous activity
        intent.setFlags(Intent.FLAG_ACTIVITY_NEW_TASK | Intent.FLAG_ACTIVITY_CLEAR_TASK);
        startActivity(intent);
    }

    /** Called when the user clicks the submit button */
    public void submitButton(View view) {
        Intent intent = new Intent(this, ProcessTransferActivity.class);
        startActivity(intent);
    }

}
