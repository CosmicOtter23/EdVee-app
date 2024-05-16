document.addEventListener('DOMContentLoaded', function() {
  // const modalTriggerElements = document.querySelectorAll('.modal-trigger');
  const modal = document.querySelector('.element-modal');
  const closeModalButton = document.getElementById('close-modal');

  // if (modal) {
  //   modalTriggerElements.forEach(element => {
  //       element.addEventListener('click', () => {
  //           modal.style.display = 'block';
  //       });
  //   });
  
  if (closeModalButton) {
    closeModalButton.addEventListener('click', () => {
        modal.style.display = 'none';
    });
  }

  // lines.forEach(line => {
  //   element.appendChild(line);
  //   console.log("Line done");
  // });

  const pdfButton = document.getElementById('pdf-button');

  if (pdfButton) {
    pdfButton.addEventListener('click', () => { 
      var element = document.getElementById('element-to-print');
      var name = "";

      // html2pdf
      name = element.getAttribute("data-value") + " - html2pdf.pdf";

      var opt = {
        margin:       0.5,
        filename:     name,
        image:        { type: 'jpeg', quality: 1 },
        html2canvas:  { scale: 1 },
        jsPDF:        { unit: 'in', format: 'letter', orientation: 'landscape' }
      };
      
      html2pdf().from(element).set(opt).save();


      // // jspdf
      // name = element.getAttribute("data-value") + " - jspdf.pdf";

      // const { jsPDF } = window.jspdf;

      // // Create a jsPDF instance
      // const pdf = new jsPDF();

      // document.getElementById('element-to-print').color = "red";
      // console.log(document.getElementById('element-to-print'));

      // // Convert the HTML element to PDF
      // pdf.html(document.getElementById('element-to-print'), {
      //   callback: function () {
      //     // Download the PDF
      //     pdf.save(name);
      //   }
      // });
    });
  }
});

function OpenDiv(divToOpen) {
  document.getElementById(divToOpen).style.display = "block";
}

function CloseDiv(divToClose) {
  document.getElementById(divToClose).style.display = "none"
}

function openTab(tabName) {
  // Hide all tab content
  var tabContents = document.querySelectorAll('.tab-content');
  tabContents.forEach(function(content) {
    content.style.display = 'none';
  });

  // Remove active class from all tabs
  var tabs = document.querySelectorAll('.tab');
  tabs.forEach(function(tab) {
    tab.classList.remove('active');
  });

  // Show the selected tab content and add active class to the clicked tab
  document.getElementById(tabName).style.display = 'block';
  event.currentTarget.classList.add('active');

  if (tabName == 'user-projects') {
    fillAllLines();
  }
  else {
    hideAllLines();
  }
}

function open_wizard_tab(evt, tabName) {
  // Declare all variables
  var i, tabcontent, tablinks;

  // Get all elements with class="tab-content" and hide them
  tabcontent = document.getElementsByClassName("tab-content");
  for (i = 0; i < tabcontent.length; i++) {
    tabcontent[i].style.display = "none";
  }

  // Get all elements with class="tab" and remove the class "active"
  tablinks = document.getElementsByClassName("tab");
  for (i = 0; i < tablinks.length; i++) {
    tablinks[i].className = tablinks[i].className.replace(" active", "");
  }

  // Show the current tab, and add an "active" class to the button that opened the tab
  document.getElementById(tabName).style.display = "block";
  evt.currentTarget.className += " active";
}

function OpenElementsNav() {
  document.getElementById("elements-button").style.display = "none";
  document.getElementById("connections-nav").style.display = "none";
  document.getElementById("elements-nav").style.display = "block";
  document.getElementById("connections-button").style.display = "block";
}

function OpenConnectionsNav() {
  document.getElementById("connections-button").style.display = "none";
  document.getElementById("elements-nav").style.display = "none";
  document.getElementById("connections-nav").style.display = "block";
  document.getElementById("elements-button").style.display = "block";
}

function HighlightButton(button) {
  // var buttons = document.getElementsByClassName('btn-nav');
  // var button = getElementById(button);

  // buttons.forEach(item => {
  //   item.style.opacity = 0.5;
  // })

  // button.style.opacity = 1;
  // button.classList.add("selected");
}

function OpenElementModal(name, desc, idNo) {
  const modal = document.querySelector('.element-modal');

  if (modal) {
    modal.style.display = 'block';

    const innerDiv = modal.querySelector('.modal-dialog, .modal-content');
  
    // Using jinja
    const header = innerDiv.querySelector('.modal-header');
    const footer = innerDiv.querySelector('.modal-footer');
    const id = header.querySelector('.form-id')
    const heading = header.querySelector('.form-control');
    const body = footer.querySelector('.form-control');
    heading.setAttribute("value", name);
    id.setAttribute("value", idNo);
    body.value = 'Description';
  
    // console.log("name: " + name + "\ndesc: " + desc + "\nid: " + idNo);
    // console.log("header: " + heading.value + "\nfooter: " + body.value + "\nid: " + id.value);
  }
}

// Lines

let boxes = Array.from(document.querySelectorAll('.line-draw'));
let clickedBoxes = [];

// Handle box click
boxes.forEach(box => {
  box.addEventListener('click', async function() {
    clickedBoxes.push(this);
    this.classList.add("selected");
    if (clickedBoxes.length === 2) {
      clickedBoxes[0].classList.remove("selected");
      clickedBoxes[1].classList.remove("selected");

      // ids = [ID1, Type1, ID2, Type2]
      ids = []
      ids.push.apply(ids, String(clickedBoxes[0].id).split("|"));
      ids.push.apply(ids, String(clickedBoxes[1].id).split("|"));

      const colour = colourPicker(ids[1], ids[3]);

      // console.log("lineExists(ids[0], ids[2]):", lineExists(ids[0], ids[2]));

      // If same box is clicked twice, cancels out as none clicked
      if (clickedBoxes[0] != clickedBoxes[1] && colour != null) {

        let line_exists = false;

        try {
          const resultArray = await getConnections();
      
          for (const index in resultArray) {
            const item = resultArray[index];
            
            // console.log("item.element1:", item.element1, "\nitem.element2:", item.element2,
            //             "\nids[0]:", String(ids[0]).split("|")[0], "\nids[2]:", ids[2])
      
            if (
              (item.element1 == String(ids[0]).split("|")[0] && item.element2 == String(ids[2]).split("|")[0]) ||
              (item.element1 == String(ids[2]).split("|")[0] && item.element2 == String(ids[0]).split("|")[0])
            ) {
              // console.log("Line found")
              line_exists = true;
            }
          }
        } 
        catch (error) {
          console.error("Error fetching data:", error);
          line_exists = true; // Return false in case of error
        }

        if (line_exists) {
          // console.log("Line not drawn - line exists")
          removeLine(clickedBoxes[0].id, clickedBoxes[1].id)
        }
        else {
          // console.log("Line being drawn - does not exist")
          drawLine(clickedBoxes[0], clickedBoxes[1], colour, false);
          recordLine(clickedBoxes[0].id, clickedBoxes[1].id);
          solidifyLines();
          // getUnconnectedNodes();
        }

      }
      clickedBoxes = [];
    }
  });
});

// Draws a line between box1 and box2 in the specified colour
function drawLine(box1, box2, colour, solid) {
  // console.log("box1:", box1, "\nbox2:", box2, "\ncolour:", colour, "\nsolid:", solid, )
  if (window.location.pathname.includes("project_wiz_3A")) {
    solid = true;
  }
  if (solid) {
    new LeaderLine(box1, box2, {color: colour, size: 2, path: 'straight', endPlug: 'behind', dropShadow: {dx: 0, dy: 0, blur: 0.5}});
  }
  else {
    new LeaderLine(box1, box2, {color: colour, size: 2, path: 'straight', endPlug: 'behind', dash: {len: 4, gap: 6, animation: true}});
  }

  // console.log("line:", line)

  // var element = document.getElementById('element-to-print');
  // element.appendChild(line);

  box1.classList.remove("red-border");
  box2.classList.remove("red-border");
  box1.classList.add("black-border");
  box2.classList.add("black-border");
  // , dropShadow: {dx: 0, dy: 0, blur: 1}
  // console.log(`Line drawn ${box1.id} -> ${box2.id}`);
}

async function removeLine(box1Id, box2Id) {  
  let response = await fetch('/api/deleteLine', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ box1Id: box1Id, box2Id: box2Id })
  });

  if (response.ok) {
    // console.log("Line deleted successfully", box1Id, box2Id);
    // Reloads page to show new arrangement of lines
    reloadPage();
  } else {
    console.error("Error deleting line: " + response.status);
  }
}

// Returns the colour of the lines needed between these two categories
function colourPicker(type1, type2) {
  if (type1 == 1 && type2 == 4 || type1 == 4 && type2 == 1) // LOS -> ASM, purple
    return "#9B2BF3";
  else if (type1 == 2 && type2 == 4 || type1 == 4 && type2 == 2) // CON -> ASM, green
    return "#64C255";
  else if (type1 == 2 && type2 == 3 || type1 == 3 && type2 == 2) // CON -> LAS, blue
    return "#179DE3";
  else if (type1 == 1 && type2 == 3 || type1 == 3 && type2 == 1) // LOS -> ASM, orange
    return "#FF796F";
  else
    return null;
}

// Gets all data stored in the Connection table as an object
async function getConnections() {
  return fetch('/get_connections')
    .then(response => response.json())
    .then(data => {
      // console.log("Data:", data);
      return data;
    })
    .catch(error => {
      console.error('Error fetching data:', error);
      throw error;
    });
}

// Gets all data stored in the Element table as an object
async function getElements() {
  return fetch('/get_elements')
    .then(response => response.json())
    .then(data => {
      // console.log("Data:", data);
      return data;
    })
    .catch(error => {
      console.error('Error fetching data:', error);
      throw error;
    });
}

function hideAllLines() {
  console.log("hiding lines")
  var leaderLineElements = document.querySelectorAll('.leader-line');

  // Loop through and remove each element
  leaderLineElements.forEach(function(element) {
    element.remove();
  });
}

// Returns true if a line already exists between the two given boxes
async function lineExists(box1Id, box2Id) {
  try {
    const resultArray = await getConnections();

    for (const index in resultArray) {
      const item = resultArray[index];

      if (
        (item.element1 === String(box1Id).split("|")[0] && item.element2 === String(box2Id).split("|")[0]) ||
        (item.element1 === String(box2Id).split("|")[0] && item.element2 === String(box1Id).split("|")[0])
      ) {
        return true;
      }
    }

    return false; // Return false if the loop completes without finding a match
  } catch (error) {
    console.error("Error fetching data:", error);
    return false; // Return false in case of error
  }
}

// Fills in all lines that exist in the database between the two given types
async function fillLines(type1, type2) {
  const data = await getConnections();
  let nodes = Array.from(document.querySelectorAll('.line-draw'));

  nodes.forEach(node => {
    node.classList.add("red-border");
  });

  for (const index in data) {
    let item = data[index];

    let IDs = [document.getElementById(item.element1 + "|" + type1), type1, 
          document.getElementById(item.element2 + "|" + type2), type2];

    if (IDs[0] && IDs[2]) {
      if (window.location.pathname.includes("project_wiz_3A")) {
        drawLine(IDs[0], IDs[2], colourPicker(IDs[1], IDs[3]), true);
      }
      else {
        drawLine(IDs[0], IDs[2], colourPicker(IDs[1], IDs[3]), false);
      }
    }

    IDs = [document.getElementById(item.element1 + "|" + type2), type2, 
          document.getElementById(item.element2 + "|" + type1), type1];

    if (IDs[0] && IDs[2]) {
      if (window.location.pathname.includes("project_wiz_3A")) {
        drawLine(IDs[0], IDs[2], colourPicker(IDs[1], IDs[3]), true);
      }
      else {
        drawLine(IDs[0], IDs[2], colourPicker(IDs[1], IDs[3]), false);
      }
    }
  }
  solidifyLines();
};

// Fill all lines between all sets of elements
function fillAllLines() {
  fillLines(1, 3);
  fillLines(3, 2);
  fillLines(2, 4);
  fillLines(4, 1);
}

// record line between the two boxes into the database
async function recordLine(box1Id, box2Id) {
  let response = await fetch('/api/recordLine', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ box1Id: box1Id, box2Id: box2Id })
  });

  if (response.ok) {
    console.log("Line recorded successfully", box1Id, box2Id);
  } else {
    console.error("Error recording line: " + response.status);
  }
}

async function solidifyLines() {
  // const elements_data = await getElements();
  // const connections_data = await getConnections();
  const elements = await getElements();
  const connections = await getConnections();

  // let elements = []
  // let connections = []

  // for (const item in elements_data) {
  //   // if (elements_data[item].project_id == 9) {
  //     elements.push(elements_data[item]);
  //     // console.log("project id:", elements_data[item].project_id);
  //   // }
  // }
  // for (const item in connections_data) {
  //   // if (connections_data[item].project_id == 9) {
  //     connections.push(connections_data[item]);
  //     // console.log("project id:", connections_data[item].project_id);
  //   // }
  // }

  // console.log("Elements:", elements);
  
  let outcomes = [];
  let contents = [];
  let activities = [];
  let assessments = [];
  
  for (const i in elements) {
    // console.log(elements[i]);
    // console.log(elements[i]['element_type']);

    if (elements[i]['element_type'] == 1) {
      outcomes.push(elements[i]);
      // console.log("0");
    }
    else if (elements[i]['element_type'] == 2) {
      contents.push(elements[i]);
    }
    else if (elements[i]['element_type'] == 3) {
      activities.push(elements[i]);
    }
    else if (elements[i]['element_type'] == 4) {
      assessments.push(elements[i]);
    }
  }

  outcomes.forEach(function(i) {
    // console.log("1");
    activities.forEach(function(j) {
      // console.log("2");
      connections.forEach(function(connection1) {
        // console.log("connection1[element1]:", connection1['element1'], "\ni.id:", i.id, "\nconnection1[element2]:", connection1['element1']);
        if (connection1['element1'] == i.id && connection1['element2'] == j.id || connection1['element1'] == j.id && connection1['element2'] == i.id) {
          // console.log("2.5");
          contents.forEach(function(k) {
            // console.log("3");
            connections.forEach(function(connection2) {
              if (connection2['element1'] == k.id && connection2['element2'] == j.id || connection2['element1'] == j.id && connection2['element2'] == k.id) {
                assessments.forEach(function(l) {
                  // console.log("4");
                  connections.forEach(function(connection3) {
                    if (connection3['element1'] == k.id && connection3['element2'] == l.id || connection3['element1'] == l.id && connection3['element2'] == k.id) {
                      outcomes.forEach(function(m) {
                        // console.log("5");
                        connections.forEach(function(connection4) {
                          if (connection4['element1'] == m.id && connection4['element2'] == l.id || connection4['element1'] == l.id && connection4['element2'] == m.id) {
                            if (i == m) {
                              // console.log("Figure of 8 found!\n", connection1, "\n", connection2, 
                              //   "\n", connection3, "\n", connection4);

                              // console.log(connection1['element1'] + "|1");

                              el1 = document.getElementById(connection1['element1'] + "|1");
                              if (!el1) {
                                el1 = document.getElementById(connection1['element2'] + "|1");
                              }
                              el2 = document.getElementById(connection2['element1'] + "|3");
                              if (!el2) {
                                el2 = document.getElementById(connection2['element2'] + "|3");
                              }
                              el3 = document.getElementById(connection3['element1'] + "|2");
                              if (!el3) {
                                el3 = document.getElementById(connection3['element2'] + "|2");
                              }
                              el4 = document.getElementById(connection4['element1'] + "|4");
                              if (!el4) {
                                el4 = document.getElementById(connection4['element2'] + "|4");
                              }
                              
                              if (el1 && el2 && el3 && el4) {
                                drawLine(el1, el2, colourPicker(1, 3), true);
                                drawLine(el2, el3, colourPicker(3, 2), true);
                                drawLine(el3, el4, colourPicker(2, 4), true);
                                drawLine(el4, el1, colourPicker(4, 1), true);
                              }
                            }
                          }
                        })
                      })
                    }
                  })
                })
              }
            })
          })
        }
      })
    })
  })
}

function getType(elementId) {
  let type = null;
  for (let i = 1; i < 5; i++) {
    if (document.getElementById(elementId + "|" + i)) {
      type = i;
      console.log("Type found:", i)
    }
  }
  return type;
}

// Add view privileges to the user
let buttons = Array.from(document.querySelectorAll('#allow-view'));
buttons.forEach(viewButton => {
  viewButton.addEventListener('click', async function() {
    userId = viewButton.value.split('|')[0]
    projectId = viewButton.value.split('|')[1]
    let response = await fetch('/api/addAccess', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ userId: userId, projectId: projectId, accessLevel: 1 })
    });
  
    if (response.ok) {
      console.log("Access recorded/updated successfully:", userId, "<->", projectId);
      reloadPage()
    } else {
      console.error("Error recording access: " + response.status);
    }
  });
});

// Add edit privileges to the user
buttons = Array.from(document.querySelectorAll('#allow-edit'));
buttons.forEach(editButton => {
  editButton.addEventListener('click', async function() {
    userId = editButton.value.split('|')[0]
    projectId = editButton.value.split('|')[1]
    let response = await fetch('/api/addAccess', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ userId: userId, projectId: projectId, accessLevel: 2 })
    });
  
    if (response.ok) {
      console.log("Access recorded/updated successfully:", userId, "<->", projectId);
      reloadPage()
    } else {
      console.error("Error recording access: " + response.status);
    }
  });
});

const navbarToggle = document.getElementById('nav-toggle');
const navbar = document.getElementById('navbar');
const content = document.getElementById('content');
const img = document.querySelector('.nav-toggle-img');

navbarToggle.addEventListener('click', () => {
  navbar.classList.toggle('collapsed');
  if (navbar.classList.contains("collapsed")) {
    // console.log("Collapsed");
    img.src = "/static/chevron-r.png";
    navbarToggle.style.transform = "translateX(2vw)";
    content.style.display = "none";
  }
  else {
    // console.log("Open");
    img.src = "/static/chevron-l.png";
    navbarToggle.style.transform = "translateX(22vw)";
    content.style.display = "block";
  }
});

function reloadPage() {
  location.reload();
}