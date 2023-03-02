package com.weddify.emailapi.entity;

public class User {
    private String firstname;
    private String lastname;
    private String email;
    private String username;
    private String servicetitle;

    public User(String firstname, String lastname, String email, String username, String servicetitle) {
        this.firstname = firstname;
        this.lastname = lastname;
        this.email = email;
        this.username = username;
        this.servicetitle = servicetitle;
    }
    public String getServicetitle() {
        return servicetitle;
    }
    public void setServicetitle(String servicetitle) {
        this.servicetitle = servicetitle;
    }
    public String getFirstname() {
        return firstname;
    }
    public void setFirstname(String firstname) {
        this.firstname = firstname;
    }
    public String getLastname() {
        return lastname;
    }
    public void setLastname(String lastname) {
        this.lastname = lastname;
    }
    public String getEmail() {
        return email;
    }
    public void setEmail(String email) {
        this.email = email;
    }
    public String getUsername() {
        return username;
    }
    public void setUsername(String username) {
        this.username = username;
    }
    @Override
    public String toString() {
        return "User [firstname=" + firstname + ", lastname=" + lastname + ", email=" + email + ", username=" + username
                + ", servicetitle=" + servicetitle + "]";
    }
    public User() {
    }
}
