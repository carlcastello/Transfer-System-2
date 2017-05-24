package com.example.transfer.Activities;

import android.app.Activity;
import android.content.Intent;
import android.support.v7.app.AlertDialog;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.view.inputmethod.InputMethodManager;
import android.widget.EditText;
import android.widget.Spinner;
import android.widget.TextView;
import android.widget.Toast;

import com.example.transfer.Controllers.TransferController;
import com.example.transfer.Interfaces.POSTListener;
import com.example.transfer.Models.Article;
import com.example.transfer.Models.User;
import com.example.transfer.R;

import org.json.JSONObject;

import java.text.SimpleDateFormat;
import java.util.Calendar;

public class ProcessTransferActivity extends AppCompatActivity implements POSTListener{

    private User user;
    private Article article;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_process_transfer);

        Intent intent = getIntent();
        this.user = (User) intent.getSerializableExtra("User");
        this.article = (Article) intent.getSerializableExtra("Article");

        // Display Title
        TextView textView1 = (TextView) findViewById(R.id.article_name_textview);
        textView1.setText(this.article.getName());

        // Display Description
        TextView textView2 = (TextView) findViewById(R.id.article_description_textview);
        textView2.setText(this.article.getDescription());

        // Display Article Number
        TextView textView3 = (TextView) findViewById(R.id.article_number_view);
        textView3.setText(this.article.getId());

        // Display Date
        // https://stackoverflow.com/questions/8654990/how-can-i-get-current-date-in-android
        Calendar c = Calendar.getInstance();
        SimpleDateFormat df = new SimpleDateFormat("MMM-dd-yyyy");
        String formattedDate = df.format(c.getTime());
        TextView textView4 = (TextView) findViewById(R.id.date_text_view);
        textView4.setText(formattedDate);
    }

    /**
     * Called when the user clicks the back button
     */
    public void backButton(View view) {
        Intent intent = new Intent(this, ReadNumberActivity.class);
        // Deletes previous activity
        intent.setFlags(Intent.FLAG_ACTIVITY_NEW_TASK | Intent.FLAG_ACTIVITY_CLEAR_TASK);
        intent.putExtra("User", this.user);
        startActivity(intent);
    }

    /**
     * Called when the user clicks the process button
     */
    public void processButton(View view) {
        boolean isLocationGiven = false;
        boolean isCountGiven = false;

        Spinner spinner = (Spinner) findViewById(R.id.spinner);
        String location = spinner.getSelectedItem().toString();

        if (location.equals("----")) {
            Toast.makeText(this,"Location is required to Transfer an article.",Toast.LENGTH_LONG).show();
        } else {
            isLocationGiven = true;
        }

        int count = 0;
        EditText editText = (EditText) findViewById(R.id.quantity_edit_view);
        try {
            count = Integer.parseInt(editText.getText().toString());
            isCountGiven = true;
        } catch (Exception error) {
            Toast.makeText(this,"Quantity is required to Transfer an article. ",Toast.LENGTH_LONG).show();
        }

        if (isCountGiven && isLocationGiven) {
            TransferController tc = new TransferController(this,this.article,location,count,this.user);
            tc.post();
        }
    }

    @Override
    public void userAuthenticated(JSONObject jsonObject){};

    @Override
    public void revertActivity() {
        View view = findViewById(android.R.id.content);
        this.backButton(view);
    }
}