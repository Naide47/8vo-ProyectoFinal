/* 
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

function ejecucion(){
    
    $(document).ready(function (){

                // SideNav Button Initialization
          $(".button-collapse").sideNav({
            breakpoint: 1200
          });
          // SideNav Scrollbar Initialization
          var sideNavScrollbar = document.querySelector('.custom-scrollbar');
          var ps = new PerfectScrollbar(sideNavScrollbar);
        
    });
    
    
}

