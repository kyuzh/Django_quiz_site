document.addEventListener('DOMContentLoaded', () => {
    fetch('/api/questions/')
        .then(response => {
            console.log('Response status:', response.status);
            return response.json();
        })
        .then(data => {
            console.log('Données reçues :', data);

            window.quizData = {
                questions: data,
                currentQuestionIndex: 0
            };

            showQuestion(window.quizData.currentQuestionIndex);
        })
        .catch(error => console.error('Erreur lors de la récupération des données :', error));

    function showQuestion(index) {
        if (window.quizData && window.quizData.questions && window.quizData.questions.length) {
            if (index >= 0 && index < window.quizData.questions.length) {
                const questionData = JSON.parse(window.quizData.questions || '{}'); // Obtenir la question spécifique
                document.getElementById('question').innerText = questionData[index].question;

                // Afficher l'index de la question
                document.getElementById('question-index').innerText = `Question ${index + 1} sur ${window.quizData.questions.length}`;
                document.getElementById('propositions').innerText = questionData[index].propositions;

                document.getElementById('answer').style.display = 'none';
                document.getElementById('explanation').style.display = 'none';
                document.getElementById('answer').innerText = questionData[index].correct_answer;
                document.getElementById('explanation').innerText = questionData[index].explanation;

                // Analyse des propositions JSON
                let propositions = {};
                try {
                    // Les propositions devraient déjà être un JSON string dans le questionData
                    propositions = JSON.parse(questionData[index].propositions || '{}');
                    console.log('Afficher les propositions :',  propositions[0]);

                    // Calculer la longueur des propositions
                    const numberOfPropositions = Object.keys(propositions[0]).length;
                    console.log('Nombre de propositions :', numberOfPropositions);

                    const propositionsContainer = document.getElementById('propositions');
                    propositionsContainer.innerHTML = '';

                    // Ajout des propositions à l'élément HTML
                    for (const key in propositions[0]) {
                        console.log('Afficher les key :',  propositions[0][key]);
                        if (propositions[0].hasOwnProperty(key) && propositions[0][key] !== null && propositions[0][key] !== 'NaN') {
                            propositionsContainer.innerHTML += `
                                <label class="list-group-item d-flex gap-2">
                                    <input class="form-check-input flex-shrink-0" type="radio" name="proposition" value="${key}">
                                    <span>${propositions[0][key]}</span>
                                </label>
                            `;
                        }
                    }
                } catch (e) {
                    console.error('Erreur lors du parsing des propositions :', e);
                }
            } else {
                console.error('Index de question hors limites');
            }
        } else {
            console.error('Données de quiz non définies ou questions manquantes');
        }
    }

    window.nextQuestion = function() {
        if (window.quizData && window.quizData.questions) {
            if (window.quizData.currentQuestionIndex < window.quizData.questions.length - 1) {
                window.quizData.currentQuestionIndex++;
                showQuestion(window.quizData.currentQuestionIndex);
            } else {
                console.warn('Dernière question atteinte');
            }
        } else {
            console.error('Données de quiz non disponibles pour passer à la question suivante');
        }
    };

    window.previousQuestion = function() {
        if (window.quizData && window.quizData.questions) {
            if (window.quizData.currentQuestionIndex > 0) {
                window.quizData.currentQuestionIndex--;
                showQuestion(window.quizData.currentQuestionIndex);
            } else {
                console.warn('Première question atteinte');
            }
        } else {
            console.error('Données de quiz non disponibles pour revenir à la question précédente');
        }
    };

    document.getElementById('go-to-question').addEventListener('click', () => {
        const questionNumber = parseInt(document.getElementById('question-number-input').value, 10);
        if (!isNaN(questionNumber) && questionNumber > 0 && questionNumber <= window.quizData.questions.length) {
            window.quizData.currentQuestionIndex = questionNumber - 1;
            showQuestion(window.quizData.currentQuestionIndex);
        } else {
            alert('Numéro de question invalide');
        }
    });

document.getElementById('show-answer').addEventListener('click', () => {
    const explanationElement = document.getElementById('explanation');
    const explanationText = explanationElement.textContent;

    // Vérification si les données du quiz existent
    if (window.quizData && window.quizData.questions) {
        document.getElementById('answer').style.display = 'block';
        explanationElement.style.display = explanationText !== "" ? 'block' : 'none'; // Afficher l'explication si elle existe
    } else {
        alert('Les données du quiz ne sont pas disponibles.');
        return;
    }

    const currentQuestionIndex = window.quizData.currentQuestionIndex;

    // Récupérer la réponse correcte pour la question actuelle
    const correctAnswer = document.getElementById('answer').textContent;

    // Récupérer la réponse sélectionnée par l'utilisateur
    const selectedOption = document.querySelector('input[name="proposition"]:checked');

    // Vérifier si l'utilisateur a sélectionné une option
    if (!selectedOption) {
        alert('Veuillez sélectionner une option avant de voir la réponse.');
        return;
    }

    const selectedAnswer = selectedOption.value;
    const selectedText = selectedOption.parentElement.querySelector('span').textContent;




    // Comparer la réponse sélectionnée avec la réponse correcte
    const label = selectedOption.parentElement;
    if (selectedText === correctAnswer) {
        selectedOption.parentElement.querySelector('span').style.color = 'green'; // Mettre en vert si c'est correct

    } else {
        selectedOption.parentElement.querySelector('span').style.color = 'red'; // Mettre en rouge si c'est incorrect

    }
});



});