package com.weddify.emailapi.service;

import java.io.File;

import javax.mail.MessagingException;
import javax.mail.internet.MimeMessage;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.core.io.FileSystemResource;
import org.springframework.mail.MailException;
import org.springframework.mail.SimpleMailMessage;
import org.springframework.mail.javamail.JavaMailSender;
import org.springframework.mail.javamail.MimeMessageHelper;
import org.springframework.stereotype.Service;
import org.thymeleaf.TemplateEngine;
import org.thymeleaf.context.Context;
import com.weddify.emailapi.entity.User;

@Service
public class EmailService {
    
    @Autowired
    private JavaMailSender mailsender;
    @Autowired
    private TemplateEngine templateEngine;

    
    public void sendEmail(String subject, String text, String to){
        try {
            SimpleMailMessage message = new SimpleMailMessage(); 
            message.setFrom("h20220293@pilani.bits-pilani.ac.in");
            message.setTo(to); 
            message.setSubject(subject); 
            message.setText(text);
            mailsender.send(message);
        } catch (MailException exception) {
            exception.printStackTrace();
        }
    }

    public void sendEmailWithAttachment(String subject, String text, String to, String pathToAttachment) {
        try {
            MimeMessage message = mailsender.createMimeMessage();
            MimeMessageHelper helper;
            helper = new MimeMessageHelper(message, true);
            helper.setFrom("h20220293@pilani.bits-pilani.ac.in");
            helper.setTo(to);
            helper.setSubject(subject);
            helper.setText(text);
                
            FileSystemResource file = new FileSystemResource(new File(pathToAttachment));
            helper.addAttachment("Invoice", file);

            mailsender.send(message);
        } 
        catch (MessagingException exception) {
            exception.printStackTrace();
        }
    }
    public void sendEmail(User user, String templateName) throws MessagingException {
        Context context = new Context();
        context.setVariable("user", user);

        String process = templateEngine.process(templateName, context);
        MimeMessage message = mailsender.createMimeMessage();
        MimeMessageHelper helper = new MimeMessageHelper(message);
        helper.setSubject("Hello " + user.getFirstname());
        helper.setText(process, true);
        helper.setTo(user.getEmail());
        helper.setFrom("h20220293@pilani.bits-pilani.ac.in");
        mailsender.send(message);
    }
}
