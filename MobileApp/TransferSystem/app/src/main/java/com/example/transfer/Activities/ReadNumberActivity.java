package com.example.transfer.Activities;

import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.EditText;
import android.widget.Toast;

import com.example.transfer.Controllers.ArticleController;
import com.example.transfer.Interfaces.GETListener;
import com.example.transfer.Models.Article;
import com.example.transfer.Models.User;
import com.example.transfer.R;

import org.json.JSONObject;

public class ReadNumberActivity extends AppCompatActivity implements GETListener{
    private User user;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_read_number);

        Intent intent = getIntent();
        this.user = (User) intent.getSerializableExtra("User");
    }

    @Override
    protected void onResume(){
        super.onResume();

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
        String articleNumber = ((EditText) findViewById(R.id.article_number_input)).getText().toString();

        ArticleController ac = new ArticleController(this,articleNumber,this.user);
        ac.get();
    }

    @Override
    public void articleExtraction(JSONObject articleJSON) {
        Article article = new Article(articleJSON);

        Intent intent = new Intent(this, ProcessTransferActivity.class);
        intent.putExtra("User", user);
        intent.putExtra("Article",article);
        startActivity(intent);
    }
}
