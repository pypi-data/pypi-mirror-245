function uid() {
    var id = "id" + Math.random().toString(16).slice(2);
    return id;
}

var clid = '';
var nowpid = ''
window.userTasksCompleted = false;
window.inputFieldValues = [];
var selectClassNames = '';
var repeated_pattern_select = window.repeated_pattern

var panel_container_name = 'panel-container-auto-wrapper-x999999999990x0x0';
var popup_container = 'popup_container';
var panel_background_color = '#0d6efd';
var mouse_hover_background_color = '#ffc107';

var basePanelTemplate = `

<div id="selector">
    <div id="selector-top"></div>
    <div id="selector-left"></div>
    <div id="selector-right"></div>
    <div id="selector-bottom"></div>
</div>

    <h2 style="font-weight:bold; color:white; font-size:14px;">Fill the form fields below by clicking on the corresponding elements in the Selenium-loaded HTML page. 
Use 'Add More' to create additional key-value pairs.</h2>
    <div id="input_panel" style="margin-top:5px;">
        
    </div>
    <div id="button_panel1" style="margin-top:5px;">
         
         <button type="button" style="float:right;" id="add_more">Add More</button> 
         
    </div>  
    
    <div id="button_panel2" style="margin-top:5px;">
         
         <button type="button" style="float:right;" id="done_action">Done</button> 
         
    </div>  

`;

var htmlTemplatetfty = `
    <div class="single_pair" style="padding:4px;">
        <input id="newAssetLiability_ID_key" class="field_key_value" placeholder="Key" name="newAssetLiability[_ID_][key]" type="text" />
        <input id="newAssetLiability_ID_value" class="field_key_value" readonly placeholder="Value" name="newAssetLiability[_ID_][value]" type="text"/>
    </div>
`;

var htmlTemplate = `
    <div class="single_pair" style="padding:4px; position: relative;" id="field_panel_ID_">
        <input id="newAssetLiability_ID_key" relId="_ID_" class="field_key_value field_key" placeholder="Select Attribute" name="newAssetLiability[_ID_][key]" type="text" />
        <input id="newAssetLiability_ID_value" relId="_ID_" class="field_key_value field_value val_ID_" readonly placeholder="Select Value" name="newAssetLiability[_ID_][value]" type="password"/>
        <input id="newAssetLiability_ID_parent" relId="_ID_" class="field_key_value field_parent parent_ID_" readonly placeholder="Select Parent" name="newAssetLiability[_ID_][parent]" type="password"/>
        <button pid="_ID_" class="fields_verify_button fields_verify_button_ID_" >Verify</button>
        <button pid="_ID_" class="fields_remove_button" style="color:#dc3545;position: absolute; right: 4px; top: 50%; transform: translateY(-50%); cursor: pointer;">✖</button>
    </div>
`;


var panel = document.createElement('div');
panel.id = panel_container_name;
panel.style.padding = '20px';
panel.style.position = 'absolute';
panel.style.top = '10px';
panel.style.right = '10px';
panel.style.width = '660px';
panel.style.zIndex = '999999999';
panel.style.borderRadius = '4px';
panel.style.backgroundColor = panel_background_color;
panel.style.borderColor = '#0d6efd';
panel.style.borderRadius = '8px';
panel.style.cursor = 'move';

var isDragging = false;
var offsetX, offsetY;

// Function to handle mouse down event
function handleMouseDown(event) {
    isDragging = true;
    // Calculate the offset between mouse position and panel position
    offsetX = event.clientX - panel.getBoundingClientRect().left;
    offsetY = event.clientY - panel.getBoundingClientRect().top;
}

// Function to handle mouse move event
function handleMouseMove(event) {
    if (isDragging) {
        // Calculate the new panel position based on mouse position and offset
        var x = event.clientX + window.scrollX - offsetX;
        var y = event.clientY + window.scrollY - offsetY;

        // Set the panel's position
        panel.style.left = x + 'px';
        panel.style.top = y + 'px';
    }
}

// Function to handle mouse up event
function handleMouseUp() {
    isDragging = false;
}

// Add event listeners for mouse events
panel.addEventListener('mousedown', handleMouseDown);
document.addEventListener('mousemove', handleMouseMove);
document.addEventListener('mouseup', handleMouseUp);



$('body').on('click', '.field_key_value', function (e) {
    clid = $(this).attr('id');
    nowpid = $(this).attr('relId');
});

// Append basePanelTemplate to the panel
panel.insertAdjacentHTML('beforeend', basePanelTemplate);

// Get the input_panel div inside the panel
var inputPanel = panel.querySelector('#input_panel');

// Append htmlTemplate under the input_panel div
var cloned_html = htmlTemplate;
var uid = uid();
cloned_html = cloned_html.replace(/_ID_/g, uid);
inputPanel.insertAdjacentHTML('beforeend', cloned_html);

// Add event listener to the "More" button
var addButton = panel.querySelector('#add_more');
addButton.addEventListener('click', function () {
    // Append htmlTemplate when the button is clicked
    var cloned_html = htmlTemplate;
    var uid = "id" + Math.random().toString(16).slice(2);
    cloned_html = cloned_html.replace(/_ID_/g, uid);
    inputPanel.insertAdjacentHTML('beforeend', cloned_html);
});

document.body.appendChild(panel);


// Append the panel to the body
document.body.appendChild(panel);

function captureClick(event) {
    var clickedElement = event.target;
    var textContent = clickedElement.textContent;
    console.log(textContent)
}

function captureHover(event) {
    var hoveredElement = event.target;
    var textContent = hoveredElement.textContent;
    alert("User hovered over: " + textContent);
}

function getXPath(element) {
    var xpath = '';
    for (; element && element.nodeType === 1; element = element.parentNode) {
        var id = 1;
        for (var sibling = element.previousSibling; sibling; sibling = sibling.previousSibling) {
            if (sibling.nodeType === 1 && sibling.tagName === element.tagName) {
                id++;
            }
        }
        id > 1 ? (id = '[' + id + ']') : (id = '');
        xpath = '/' + element.tagName.toLowerCase() + id + xpath;
    }
    
    // Use document.evaluate to get the text value using XPath
    var text = document.evaluate('string(' + xpath + ')', document, null, XPathResult.STRING_TYPE, null).stringValue;
    
    // Return both XPath and text value
    return { xpath: xpath, text: text.trim() };
}

function getLastInnerClassNames__qsasqs(event) {
    var current = event.srcElement || event.originalTarget;
    // Traverse to the most inner element with a class
    while (current.lastElementChild && current.lastElementChild.className.trim() !== '') {
        current = current.lastElementChild;
    }
    if (current.className.trim() !== '') {
        // Extract and alert the class names
        var innerClassNames = current.className.split(' ').join(' ');
        selectClassNames = innerClassNames;
    } else {
        alert('No inner element with a class found.');
        selectClassNames = '';
    }
    
}
//text-success text-bold text-antialiased
//text-accent text-bold text-antialiased
function getLastInnerClassNames(event) {
    selectClassNames = '';
    var target = event.srcElement || event.originalTarget;
    // Ensure the target has a parent node
    if (target.parentNode) {
        var parentClassNames = target.parentNode.className.trim();
        
        if (parentClassNames !== '') {
            // Extract and log the class names
            console.log(parentClassNames);
            selectClassNames = parentClassNames;
        } else {
            console.log('Parent element has no class.');
        }
    } else {
        console.log('No parent element found.');
        
    }
}

function generateRelativeClassNames(event) {
    selectClassNames = ''
    
    var hierarchy = [],
        current = event.srcElement || event.originalTarget;

    while (current.parentNode) {
        hierarchy.unshift(current);
        current = current.parentNode;
    }

    var xPathSegments = hierarchy.map(function (el) {
        return ((el.className !== '') ? '.' + el.className.split(' ').join('.') : '');
    });
    if(xPathSegments.length >0){
        selectClassNames =  xPathSegments[xPathSegments.length - 1];
    }
    
    return selectClassNames;
}


document.addEventListener('mouseover', function (event) {
    var target = event.target;
    if (!isInjectedButton(target)) {
        //var path = getXPath(target);
        //console.log(path);
        target.style.backgroundColor = mouse_hover_background_color;
    }
});

document.addEventListener('mouseout', function (event) {
    var target = event.target;
    if (!isInjectedButton(target)) {
        target.style.backgroundColor = ''; // Reset background color when mouseout
    }
});


document.addEventListener('contextmenu', generateRelativeClassNames);

document.addEventListener('contextmenu', function (event) {
    var target = event.target;
    if (!isInjectedButton(target)) {
        $('.fields_verify_button'+nowpid).css('background-color', '#dc3545');
        $('.fields_verify_button'+nowpid).text('Verify');
        var path = getXPath(target);
        if(clid != ''){
            if(clid.includes('key')){
                $('#'+clid).val(path.text);
            }else{
                if(repeated_pattern_select=='yes'){
                    $('#'+clid).val(selectClassNames);
                }else{
                    $('#'+clid).val(path.xpath);
                }
            }
        }
        event.preventDefault();
        return false;
    }
});

$('body').on('click', '.fields_remove_button', function (e) {
    pid = $(this).attr('pid');
    $('#field_panel'+pid).remove();
});

$('body').on('click', '.fields_verify_button', function (e) {
    pid = $(this).attr('pid');
    nowpid = pid;
    bclass = $('#newAssetLiability' + pid + 'parent').val();
    cclass = $('#newAssetLiability' + pid + 'value').val();
    var innermostText = '';
    b = 0;
    
    if(repeated_pattern_select !='yes'){
        var resultpath = document.evaluate(cclass, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null);
        if (resultpath.singleNodeValue) {
            foundElement = resultpath.singleNodeValue;
            innermostText = foundElement.textContent;
        }else{
            innermostText = '';
        }
        
    }else{
        $(bclass).each(function () {
            if(b<5){
                innermostText = innermostText + $(this).find(cclass).text() + '\n';
            }
            b = b + 1;
        });
    }
    
    
    jConfirm('Is the following sample data collection correct based on your selection?\n' + innermostText, 'Confirmation Dialog', function(r) {
        if (r) {
            $('.fields_verify_button'+pid).css('background-color', '#155724');
            $('.fields_verify_button'+pid).text('Verified');
        } else {
            $('.fields_verify_button'+pid).css('background-color', '#dc3545');
            $('.fields_verify_button'+pid).text('Verify');
            jAlert('Let\'s try again by diiferent way!', 'Alert Dialog');
        }
    });
    
});

var doneButton = panel.querySelector('#done_action');
doneButton.addEventListener('click', function () {
    window.userTasksCompleted = true;
    console.log('User tasks completed:', window.userTasksCompleted);
   
    var allPairs = document.querySelectorAll('.single_pair');
    allPairs.forEach(function(pairElement) {
        // Get key and value for each pair
        var keyInput = pairElement.querySelector('.field_key');
        var valueInput = pairElement.querySelector('.field_value');
        var parentInput = pairElement.querySelector('.field_parent');
        
        //alert(keyInput.value + valueInput.value + parentInput.value)

        // Store the values in the array
        var fieldValue = {
            attribute_name: keyInput.value,
            attribute_value: valueInput.value,
            attribute_value_parent: parentInput.value
        };
        window.inputFieldValues.push(fieldValue);
    });
    
});


function isInjectedButton(element) {
    var menuContainer = document.getElementById(panel_container_name);
    var popup_container_data = document.getElementById(popup_container);
    //return menuContainer.contains(element) || popup_container.contains(element);
    if(popup_container_data){
        if(menuContainer.contains(element) || popup_container_data.contains(element)){
            return true;
        }
    }else{
        if(menuContainer.contains(element)){
            return true;
        }
    }
    return false;
}

var elements = {
    top: $('#selector-top'),
    left: $('#selector-left'),
    right: $('#selector-right'),
    bottom: $('#selector-bottom')
};

$(document).mousemove(function(event) {
    return;
    if (isInjectedButton(event.target)) {
        return;
    }
    if(event.target.id.indexOf('selector') !== -1 || event.target.tagName === 'BODY' || event.target.tagName === 'HTML') return;
    
    var $target = $(event.target);
        targetOffset = $target[0].getBoundingClientRect(),
        targetHeight = targetOffset.height,
        targetWidth  = targetOffset.width;
    console.log(targetOffset);
    
    elements.top.css({
        left:  (targetOffset.left - 4),
        top:   (targetOffset.top - 4),
        width: (targetWidth + 5)
    });
    elements.bottom.css({
        top:   (targetOffset.top + targetHeight + 1),
        left:  (targetOffset.left  - 3),
        width: (targetWidth + 4)
    });
    elements.left.css({
        left:   (targetOffset.left  - 5),
        top:    (targetOffset.top  - 4),
        height: (targetHeight + 8)
    });
    elements.right.css({
        left:   (targetOffset.left + targetWidth + 1),
        top:    (targetOffset.top  - 4),
        height: (targetHeight + 8)
    });
    
});

function getElementByXpath(path) {
  return document.evaluate(
    path,
    document,
    null,
    XPathResult.FIRST_ORDERED_NODE_TYPE,
    null
  ).singleNodeValue;
}
