$(document).ready(function() {
    $('#entryForm').on('submit', function(e) {
        let description = $('#description').val().trim();
        if(description === '') {
            alert('Please write something before submitting!');
            e.preventDefault();
        } else {
            $('#successMessage').fadeIn(500).delay(2000).fadeOut(500);
        }
    });

    $('#registerForm').on('submit', function(e) {
        let username = $('#username').val().trim();
        let password = $('#password').val();
        let emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

        if(username === '' || password === '') {
            alert('Username and password cannot be empty');
            e.preventDefault();
            return;
        }

        if(!emailPattern.test(username)) {
            alert('Please enter a valid email address');
            e.preventDefault();
            return;
        }

        let passwordPattern = /^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{6,}$/;
        if(!passwordPattern.test(password)) {
            alert('Password must be at least 6 characters long and include at least 1 letter and 1 number');
            e.preventDefault();
            return;
        }
    });

    $('#loginForm').on('submit', function(e) {
        let username = $('#username').val().trim();
        let password = $('#password').val().trim();
        if(username === '' || password === '') {
            alert('Please fill in both username and password');
            e.preventDefault();
        }
    });

    $('input, textarea').focus(function() {
        $(this).css('border-color', '#000').animate({ paddingLeft: '10px' }, 200);
    }).blur(function() {
        $(this).css('border-color', '').animate({ paddingLeft: '5px' }, 200);
    });
});

