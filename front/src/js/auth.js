
// 点击登录按钮，弹出模态对话框
// $(function () {
//     $("#btn").click(function () {
//         $(".mask-wrapper").show();
//     });
//
//     $(".close-btn").click(function () {
//         $(".mask-wrapper").hide();
//     });
// });


$(function () {
    $(".switch").click(function () {
        var scrollWrapper = $(".scroll-wrapper");
        var currentLeft = scrollWrapper.css("left");
        currentLeft = parseInt(currentLeft);
        if(currentLeft < 0){
            scrollWrapper.animate({"left":'0'});
        }else{
            scrollWrapper.animate({"left":"-400px"});
        }
    });
});

function  Auth() {
    var self=this;
    self.maskWrapper=$('.mask-wrapper');
}

Auth.prototype.run=function () {
    var self=this;
    self.listenShowHideEvent();
};
Auth.prototype.showEvent=function () {
    var self=this;
    self.maskWrapper.show();
};
Auth.prototype.hideEvent=function () {
    var self=this;
    self.maskWrapper.hide();
};
Auth.prototype.listenShowHideEvent=function(){
    var self=this;
    var signinBtn=$('signin-btn');
    var signupBtn=$('.signup-btn');
    var closeBtn=$('.close-btn');
    var scrollWrapper=$('.scroll-wrapper');

    signinBtn.onclick(function () {
        self.showEvent();
        scrollWrapper.css({"left":0})
    });
    signupBtn.onclick(function () {
        self.showEvent();
        scrollWrapper.css({"left":-400})
    });
    closeBtn.onclick(function () {
        self.hideEvent();
    });
};


$(function () {
    var auth=new Auth();
    auth.run();
});