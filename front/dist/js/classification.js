function Li() {
    var self=this;
}

Li.prototype.listenClick = function () {
    var tabGroup = $(".nav-list");
tabGroup.children().click(function () {
    var li = $(this);
    li.addClass('active').siblings().removeClass('active');
});
}

Li.prototype.run = function(){
    var self = this;
    self.listenClick();
}

function FrontBase2() {
    var self = this;
}

FrontBase2.prototype.LiaddClass = function(){
  var li = $("#ketang");
  li.addClass('active').siblings().removeClass('active');
};

FrontBase2.prototype.run = function(){
  var self = this;
  self.LiaddClass();
};


$(function () {
   var f = new FrontBase2();
    f.run();
});


$(function () {
    var li = new Li();
    li.run();
})