   **Παραλλαγή του CTGOV-02: Συχνά Φάρμακα για την αντιμετώπιση μιας συγκεκριμένης Ασθένειας**

   >Να φτιάξετε μια δικτυακή εφαρμογή η οποία βρίσκει *όλα* τα φάρμακα που έχουν χορηγηθεί (element: intervention) για την αντιμετώπιση μιας συγκεκριμένης ασθένειας.
   >Το input θα είναι το όνομα της ασθένειας το οποίο θα το ορίζει ο χρήστης μέσω της web σελίδας και το output θα είναι το *100 (max)* πιο συχνά φάρμακα (για την ακρίβεια, φαρμακευτικές ουσίες) καθώς και η συχνότητα χρήσης τους.
   >Για τις ανάγκες τις εφαρμογής αυτής θα χρειαστεί να κατεβάσετε όλες τις διαθέσιμες κλινικές δοκιμές (XML αρχεία) από το https://clinicaltrials.gov/ ώστε αρχικά να φιλτράρετε τις κλινικές μελέτες με βάση την ασθένεια και έπειτα να βρείτε τα “top” φάρμακα.

Ο χρήστης θα διαλέγει είτε:
-να πάρει κατευθείαν τα αποτελέσματα των *100* πιο συχνά χορηγούμενων φαρμάκων, ή 
-να προσπαθήσει να μαντέψει σε ένα παιχνίδι (τύπου "Άκου τι Είπαν"/"Family Feud") από ΌΛΑ τα φάρμακα που έχουν χορηγηθεί για την ασθένεια.

Τα κορυφαία σκορ θα αποθηκεύονται σε βάση και θα εμφανίζονται στην αρχική σελίδα.

Τεχνολογίες - Vue για το frontend, Flask για το backend/services, MongoDB για τη βάση.

http://147.102.19.19/wordpress/%ce%bf%ce%b4%ce%b7%ce%b3%ce%af%ce%b5%cf%82-%cf%83%cf%85%ce%bc%ce%bc%ce%b5%cf%84%ce%bf%cf%87%ce%ae%cf%82/

## Deployment
*Requirements*:
1. npm (version 6.13.4)
2. Python (version 3.8.3)
3. Docker (version 19.03.12) with mongoDB (version 4.2.8)

Start a Docker container that houses the mongoDB database:   
    docker run -d --name base -v /data/db -p 27017:27017 mongo

Copy the collection JSON into the container:   
    docker cp  ./Studies.json base:/tmp/Studies.json

Access the container and import the collection to the database:   
    docker exec -it base /bin/bash   
    mongoimport -d local -c Studies /tmp/Studies.json   
*Optional*: Import the Accounts and Scores collections from their respective JSON files.   

Activate the virtual environment and run the Flask server file:   
    source ./env/Scripts/activate   
    python app.py   
*Note"*: make sure you run the file using python 3.\*.   

Activate the vue client:   
    npm run build   

Access the app on http://localhost/8080/page .   
