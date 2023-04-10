package com.weddify.emailapi.controller;

import javax.mail.MessagingException;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.mail.SimpleMailMessage;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import com.weddify.emailapi.entity.User;
import com.weddify.emailapi.service.EmailService;

@RestController
public class EmailController {

    @Autowired
    private EmailService EmailService;

    @RequestMapping("/welcome")
    public void welcome(){
        this.EmailService.sendEmail("Welcome","Welcome to my email service","sparsh.kr14@gmail.com");
    }

    @PostMapping("/register")
    public void registerEmail(@RequestBody User user) throws MessagingException {
        
        try {
            EmailService.sendEmail(user, "WelcomeEmail");
        } catch (MessagingException e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
        }
    }

    @PostMapping("/book")
    public void BookEmail(@RequestBody User user){
        
        try {
            this.EmailService.sendEmail(user, "BookingEmail");
        } catch (MessagingException e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
        }
        
    }

    @PostMapping("/bookvendor")
    public void BookEmailVendor(@RequestBody User user){
        
        try {
            this.EmailService.sendEmail(user, "BookingEmailVendor");
        } catch (MessagingException e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
        }
        
    }

    @PostMapping("/cancelbook")
    public void BookCancelEmail(@RequestBody User user){
        
        try {
            this.EmailService.sendEmail(user, "BookingCancelEmail");
        } catch (MessagingException e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
        }
        
    }

    @PostMapping("/cancelbookvendor")
    public void BookCancelEmailVendor(@RequestBody User user){
        
        try {
            this.EmailService.sendEmail(user, "BookingCancelEmailVendor");
        } catch (MessagingException e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
        }
        
    }

    @PostMapping("/delete")
    public void DeleteEmail(@RequestBody User user){
        
        try {
            this.EmailService.sendEmail(user, "GoodbyeEmail");
        } catch (MessagingException e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
        }
        
    }

    @PostMapping("/resetpwd")
    public void ResetpwdEmail(@RequestBody User user){
        
        try {
            this.EmailService.sendEmail(user, "ResetpwdEmail");
        } catch (MessagingException e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
        }
        
    }
}