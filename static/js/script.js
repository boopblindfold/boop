var questionList = document.getElementsByTagName("ol");
var qNumber = 3
var addBtn = document.getElementById("addQuestion");

addBtn.addEventListener("click", addQuestion());

function addQuestion(){


    var listItem = document.createElement("li");
        listItem.id = "Question"+qNumber + "";

    var questionInput = document.createElement("input");
    	questionInput.className = "question"
    	questionInput.type="text";

    var removeBtn = document.createElement("button");
		removeBtn.className = "removeQuestion"
        removeBtn.id="removeBtn"+qNumber
        removeBtn.onclick = function (e) {
    					                   var parent = this.parentNode
    						               var grParent = parent.parentNode
                						   grParent.removeChild(parent);
    			     		};
    	removeBtn.innerHTML = "Remove Question";

    listItem.appendChild(questionInput);
	listItem.appendChild(removeBtn);
	listItem.appendChild(document.createElement("br"))

    var form = document.createElement("form")

    var answerTypes = ["Likert", "Radio", "Scroller", "Slider", "Text"]

    for (var i = 1; i <= 4; i++)
    {
    	var answerType = document.createElement("label")
    	    answerType.innerHTML = answerTypes[i];
    		answerType.type= "radio"
    		answerType.name= answerTypes[i];
			answerType.class="answerType"
			answerType.id= answerTypes[i];
    		form.appendChild(answerType)
    		form.appendChild(document.createElement("input"))
			form.appendChild(document.createElement("br"))
    		listItem.appendChild(form)
    }
    
    listItem.appendChild(document.createElement("br"))
    questionList[0].appendChild(listItem);
    qNumber ++;
}

