package com.example.transfer.Models;

import org.json.JSONObject;

import java.io.Serializable;

/**
 * Created by carlcastello on 23/05/17.
 */

public class Article implements Serializable {
    private static final long serialVersionUID = 1L;

    private String id;
    private String name;
    private String description;
    private double price;

    public Article(JSONObject articleJSON) {
        // http://hmkcode.com/android-passing-java-object-another-activity/
        try {
            this.id = articleJSON.getString("id");
            this.name = articleJSON.getString("name");
            this.description = articleJSON.getString("description");
            this.price = articleJSON.getDouble("price");
        } catch (Exception error) {
            System.out.println(error);
        }
    }

    public String getName() {
        return this.name;
    }

    public String getId() {
        return id;
    }

    public String getDescription() {
        return description;
    }

    public double getPrice() {
        return price;
    }

    public String toString() {
        return "Article [ id=" + this.id + ", name=" + this.name + ", description=" +
                this.description + ", price=" + this.price + "]";
    }

}
