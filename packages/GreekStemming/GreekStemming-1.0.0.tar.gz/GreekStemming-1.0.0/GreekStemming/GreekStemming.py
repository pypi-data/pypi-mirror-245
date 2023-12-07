import re


class GreekStemming:
    cases = dict()
    cases["ΦΑΓΙΑ"] = "ΦΑ"
    cases["ΦΑΓΙΟΥ"] = "ΦΑ"
    cases["ΦΑΓΙΩΝ"] = "ΦΑ"
    cases["ΣΚΑΓΙΑ"] = "ΣΚΑ"
    cases["ΣΚΑΓΙΟΥ"] = "ΣΚΑ"
    cases["ΣΚΑΓΙΩΝ"] = "ΣΚΑ"
    cases["ΟΛΟΓΙΟΥ"] = "ΟΛΟ"
    cases["ΟΛΟΓΙΑ"] = "ΟΛΟ"
    cases["ΟΛΟΓΙΩΝ"] = "ΟΛΟ"
    cases["ΣΟΓΙΟΥ"] = "ΣΟ"
    cases["ΣΟΓΙΑ"] = "ΣΟ"
    cases["ΣΟΓΙΩΝ"] = "ΣΟ"
    cases["ΤΑΤΟΓΙΑ"] = "ΤΑΤΟ"
    cases["ΤΑΤΟΓΙΟΥ"] = "ΤΑΤΟ"
    cases["ΤΑΤΟΓΙΩΝ"] = "ΤΑΤΟ"
    cases["ΚΡΕΑΣ"] = "ΚΡΕ"
    cases["ΚΡΕΑΤΟΣ"] = "ΚΡΕ"
    cases["ΚΡΕΑΤΑ"] = "ΚΡΕ"
    cases["ΚΡΕΑΤΩΝ"] = "ΚΡΕ"
    cases["ΠΕΡΑΣ"] = "ΠΕΡ"
    cases["ΠΕΡΑΤΟΣ"] = "ΠΕΡ"
    cases["ΠΕΡΑΤΑ"] = "ΠΕΡ"
    cases["ΠΕΡΑΤΩΝ"] = "ΠΕΡ"
    cases["ΤΕΡΑΣ"] = "ΤΕΡ"
    cases["ΤΕΡΑΤΟΣ"] = "ΤΕΡ"
    cases["ΤΕΡΑΤΑ"] = "ΤΕΡ"
    cases["ΤΕΡΑΤΩΝ"] = "ΤΕΡ"
    cases["ΦΩΣ"] = "ΦΩ"
    cases["ΦΩΤΟΣ"] = "ΦΩ"
    cases["ΦΩΤΑ"] = "ΦΩ"
    cases["ΦΩΤΩΝ"] = "ΦΩ"
    cases["ΚΑΘΕΣΤΩΣ"] = "ΚΑΘΕΣΤ"
    cases["ΚΑΘΕΣΤΩΤΟΣ"] = "ΚΑΘΕΣΤ"
    cases["ΚΑΘΕΣΤΩΤΑ"] = "ΚΑΘΕΣΤ"
    cases["ΚΑΘΕΣΤΩΤΩΝ"] = "ΚΑΘΕΣΤ"
    cases["ΓΕΓΟΝΟΣ"] = "ΓΕΓΟΝ"
    cases["ΓΕΓΟΝΟΤΟΣ"] = "ΓΕΓΟΝ"
    cases["ΓΕΓΟΝΟΤΑ"] = "ΓΕΓΟΝ"
    cases["ΓΕΓΟΝΟΤΩΝ"] = "ΓΕΓΟΝ"
    vowels = "[ΑΕΗΙΟΥΩ]"
    refinedVowels = "[ΑΕΗΙΟΩ]"

    @staticmethod
    def stemWord(w: str, banned: set):

        stem = None
        suffix = None
        test1 = True

        if len(w) < 4 or w in banned:
            return w

        pattern = None
        pattern2 = None
        pattern3 = None
        pattern4 = None

        # Step1
        pattern = re.compile(
            r"(.*)(ΦΑΓΙΑ|ΦΑΓΙΟΥ|ΦΑΓΙΩΝ|ΣΚΑΓΙΑ|ΣΚΑΓΙΟΥ|ΣΚΑΓΙΩΝ|ΟΛΟΓΙΟΥ|ΟΛΟΓΙΑ|ΟΛΟΓΙΩΝ|ΣΟΓΙΟΥ|ΣΟΓΙΑ|ΣΟΓΙΩΝ|ΤΑΤΟΓΙΑ|ΤΑΤΟΓΙΟΥ|ΤΑΤΟΓΙΩΝ|ΚΡΕΑΣ|ΚΡΕΑΤΟΣ|ΚΡΕΑΤΑ|ΚΡΕΑΤΩΝ|ΠΕΡΑΣ|ΠΕΡΑΤΟΣ|ΠΕΡΑΤΑ|ΠΕΡΑΤΩΝ|ΤΕΡΑΣ|ΤΕΡΑΤΟΣ|ΤΕΡΑΤΑ|ΤΕΡΑΤΩΝ|ΦΩΣ|ΦΩΤΟΣ|ΦΩΤΑ|ΦΩΤΩΝ|ΚΑΘΕΣΤΩΣ|ΚΑΘΕΣΤΩΤΟΣ|ΚΑΘΕΣΤΩΤΑ|ΚΑΘΕΣΤΩΤΩΝ|ΓΕΓΟΝΟΣ|ΓΕΓΟΝΟΤΟΣ|ΓΕΓΟΝΟΤΑ|ΓΕΓΟΝΟΤΩΝ)$")

        if pattern.match(w):
            fp = pattern.match(w).groups()
            stem = fp[0]
            suffix = fp[1]
            w = stem + GreekStemming.cases[suffix]
            test1 = False

        # Step 2a
        pattern = re.compile(r"^(.+?)(ΑΔΕΣ|ΑΔΩΝ)$")
        if pattern.match(w):
            fp = pattern.match(w).groups()
            stem = fp[0]
            w = stem
            reg1 = re.compile(r"(ΟΚ|ΜΑΜ|ΜΑΝ|ΜΠΑΜΠ|ΠΑΤΕΡ|ΓΙΑΓΙ|ΝΤΑΝΤ|ΚΥΡ|ΘΕΙ|ΠΕΘΕΡ)$")

            if not reg1.match(w):
                w = w + "ΑΔ"

        # Step 2b
        pattern2 = re.compile(r"^(.+?)(ΕΔΕΣ|ΕΔΩΝ)$")
        if pattern2.match(w):
            fp = pattern2.match(w).groups()
            stem = fp[0]
            w = stem
            except2 = re.compile(r"(ΟΠ|ΙΠ|ΕΜΠ|ΥΠ|ΓΗΠ|ΔΑΠ|ΚΡΑΣΠ|ΜΙΛ)$")
            if except2.match(w):
                w = w + "ΕΔ"

        # Step 2c
        pattern3 = re.compile(r"^(.+?)(ΟΥΔΕΣ|ΟΥΔΩΝ)$")
        if pattern3.match(w):
            fp = pattern3.match(w).groups()
            stem = fp[0]
            w = stem
            except3 = re.compile(r"(ΑΡΚ|ΚΑΛΙΑΚ|ΠΕΤΑΛ|ΛΙΧ|ΠΛΕΞ|ΣΚ|Σ|ΦΛ|ΦΡ|ΒΕΛ|ΛΟΥΛ|ΧΝ|ΣΠ|ΤΡΑΓ|ΦΕ)$")
            if except3.match(w):
                w = w + "ΟΥΔ"

        # Step 2d
        pattern4 = re.compile("^(.+?)(ΕΩΣ|ΕΩΝ)$")
        if pattern4.match(w):
            fp = pattern4.match(w).groups()
            stem = fp[0]
            w = stem
            test1 = False
            except4 = re.compile(r"^(Θ|Δ|ΕΛ|ΓΑΛ|Ν|Π|ΙΔ|ΠΑΡ)$")
            if except4.match(w):
                w = w + "Ε"

        # Step 3
        pattern = re.compile(r"^(.+?)(ΙΑ|ΙΟΥ|ΙΩΝ)$")
        if pattern.match(w):
            fp = pattern.match(w).groups()
            stem = fp[0]
            w = stem
            pattern2 = re.compile(GreekStemming.vowels + "$")
            test1 = False
            if pattern2.match(w):
                w = stem + "Ι"

        # Step 4
        pattern = re.compile(r"^(.+?)(ΙΚΑ|ΙΚΟ|ΙΚΟΥ|ΙΚΩΝ)$")
        if pattern.match(w):
            fp = pattern.match(w).groups()
            stem = fp[0]
            w = stem
            test1 = False
            pattern2 = re.compile(GreekStemming.vowels + "$")
            except5 = re.compile(
                r"^(ΑΛ|ΑΔ|ΕΝΔ|ΑΜΑΝ|ΑΜΜΟΧΑΛ|ΗΘ|ΑΝΗΘ|ΑΝΤΙΔ|ΦΥΣ|ΒΡΩΜ|ΓΕΡ|ΕΞΩΔ|ΚΑΛΠ|ΚΑΛΛΙΝ|ΚΑΤΑΔ|ΜΟΥΛ|ΜΠΑΝ|ΜΠΑΓΙΑΤ|ΜΠΟΛ|ΜΠΟΣ|ΝΙΤ|ΞΙΚ|ΣΥΝΟΜΗΛ|ΠΕΤΣ|ΠΙΤΣ|ΠΙΚΑΝΤ|ΠΛΙΑΤΣ|ΠΟΣΤΕΛΝ|ΠΡΩΤΟΔ|ΣΕΡΤ|ΣΥΝΑΔ|ΤΣΑΜ|ΥΠΟΔ|ΦΙΛΟΝ|ΦΥΛΟΔ|ΧΑΣ)$")
            if except5.match(w) or pattern2.match(w):
                w = w + "ΙΚ"

        # step 5a
        pattern = re.compile(r"^(.+?)(ΑΜΕ)$")
        pattern2 = re.compile(r"^(.+?)(ΑΓΑΜΕ|ΗΣΑΜΕ|ΟΥΣΑΜΕ|ΗΚΑΜΕ|ΗΘΗΚΑΜΕ)$")
        if w == "ΑΓΑΜΕ":
            w = "ΑΓΑΜ"

        if pattern2.match(w):
            fp = pattern2.match(w).groups()
            stem = fp[0]
            w = stem
            test1 = False

        if pattern.match(w):
            fp = pattern.match(w).groups()
            stem = fp[0]
            w = stem
            test1 = False
            except6 = re.compile(r"^(ΑΝΑΠ|ΑΠΟΘ|ΑΠΟΚ|ΑΠΟΣΤ|ΒΟΥΒ|ΞΕΘ|ΟΥΛ|ΠΕΘ|ΠΙΚΡ|ΠΟΤ|ΣΙΧ|Χ)$")
            if except6.match(w):
                w = w + "ΑΜ"

        # Step 5b
        pattern2 = re.compile(r"^(.+?)(ΑΝΕ)$")
        pattern3 = re.compile(r"^(.+?)(ΑΓΑΝΕ|ΗΣΑΝΕ|ΟΥΣΑΝΕ|ΙΟΝΤΑΝΕ|ΙΟΤΑΝΕ|ΙΟΥΝΤΑΝΕ|ΟΝΤΑΝΕ|ΟΤΑΝΕ|ΟΥΝΤΑΝΕ|ΗΚΑΝΕ|ΗΘΗΚΑΝΕ)$")
        if pattern3.match(w):
            fp = pattern3.match(w).groups()
            stem = fp[0]
            w = stem
            test1 = False
            pattern3 = re.compile(r"^(ΤΡ|ΤΣ)$")
            if pattern3.match(w):
                w = w + "ΑΓΑΝ"

        if pattern2.match(w):
            fp = pattern2.match(w).groups()
            stem = fp[0]
            w = stem
            test1 = False
            pattern2 = re.compile(GreekStemming.refinedVowels + "$")
            except7 = re.compile(
                r"^(ΒΕΤΕΡ|ΒΟΥΛΚ|ΒΡΑΧΜ|Γ|ΔΡΑΔΟΥΜ|Θ|ΚΑΛΠΟΥΖ|ΚΑΣΤΕΛ|ΚΟΡΜΟΡ|ΛΑΟΠΛ|ΜΩΑΜΕΘ|Μ|ΜΟΥΣΟΥΛΜ|Ν|ΟΥΛ|Π|ΠΕΛΕΚ|ΠΛ|ΠΟΛΙΣ|ΠΟΡΤΟΛ|ΣΑΡΑΚΑΤΣ|ΣΟΥΛΤ|ΤΣΑΡΛΑΤ|ΟΡΦ|ΤΣΙΓΓ|ΤΣΟΠ|ΦΩΤΟΣΤΕΦ|Χ|ΨΥΧΟΠΛ|ΑΓ|ΟΡΦ|ΓΑΛ|ΓΕΡ|ΔΕΚ|ΔΙΠΛ|ΑΜΕΡΙΚΑΝ|ΟΥΡ|ΠΙΘ|ΠΟΥΡΙΤ|Σ|ΖΩΝΤ|ΙΚ|ΚΑΣΤ|ΚΟΠ|ΛΙΧ|ΛΟΥΘΗΡ|ΜΑΙΝΤ|ΜΕΛ|ΣΙΓ|ΣΠ|ΣΤΕΓ|ΤΡΑΓ|ΤΣΑΓ|Φ|ΕΡ|ΑΔΑΠ|ΑΘΙΓΓ|ΑΜΗΧ|ΑΝΙΚ|ΑΝΟΡΓ|ΑΠΗΓ|ΑΠΙΘ|ΑΤΣΙΓΓ|ΒΑΣ|ΒΑΣΚ|ΒΑΘΥΓΑΛ|ΒΙΟΜΗΧ|ΒΡΑΧΥΚ|ΔΙΑΤ|ΔΙΑΦ|ΕΝΟΡΓ|ΘΥΣ|ΚΑΠΝΟΒΙΟΜΗΧ|ΚΑΤΑΓΑΛ|ΚΛΙΒ|ΚΟΙΛΑΡΦ|ΛΙΒ|ΜΕΓΛΟΒΙΟΜΗΧ|ΜΙΚΡΟΒΙΟΜΗΧ|ΝΤΑΒ|ΞΗΡΟΚΛΙΒ|ΟΛΙΓΟΔΑΜ|ΟΛΟΓΑΛ|ΠΕΝΤΑΡΦ|ΠΕΡΗΦ|ΠΕΡΙΤΡ|ΠΛΑΤ|ΠΟΛΥΔΑΠ|ΠΟΛΥΜΗΧ|ΣΤΕΦ|ΤΑΒ|ΤΕΤ|ΥΠΕΡΗΦ|ΥΠΟΚΟΠ|ΧΑΜΗΛΟΔΑΠ|ΨΗΛΟΤΑΒ)$")
            if (pattern2.match(w)) or (except7.match(w)):
                w = w + "ΑΝ"

        # //Step 5c
        pattern3 = re.compile(r"^(.+?)(ΕΤΕ)$")
        pattern4 = re.compile(r"^(.+?)(ΗΣΕΤΕ)$")
        if pattern4.match(w):
            fp = pattern4.match(w).groups()
            stem = fp[0]
            w = stem
            test1 = False

        if pattern3.match(w):
            fp = pattern3.match(w).groups()
            stem = fp[0]
            w = stem
            test1 = False
            pattern3 = re.compile(GreekStemming.refinedVowels + "$")
            except8 = re.compile(
                r"(ΟΔ|ΑΙΡ|ΦΟΡ|ΤΑΘ|ΔΙΑΘ|ΣΧ|ΕΝΔ|ΕΥΡ|ΤΙΘ|ΥΠΕΡΘ|ΡΑΘ|ΕΝΘ|ΡΟΘ|ΣΘ|ΠΥΡ|ΑΙΝ|ΣΥΝΔ|ΣΥΝ|ΣΥΝΘ|ΧΩΡ|ΠΟΝ|ΒΡ|ΚΑΘ|ΕΥΘ|ΕΚΘ|ΝΕΤ|ΡΟΝ|ΑΡΚ|ΒΑΡ|ΒΟΛ|ΩΦΕΛ)$")
            except9 = re.compile(
                r"^(ΑΒΑΡ|ΒΕΝ|ΕΝΑΡ|ΑΒΡ|ΑΔ|ΑΘ|ΑΝ|ΑΠΛ|ΒΑΡΟΝ|ΝΤΡ|ΣΚ|ΚΟΠ|ΜΠΟΡ|ΝΙΦ|ΠΑΓ|ΠΑΡΑΚΑΛ|ΣΕΡΠ|ΣΚΕΛ|ΣΥΡΦ|ΤΟΚ|Υ|Δ|ΕΜ|ΘΑΡΡ|Θ)$")
            if (pattern3.match(w)) or (except8.match(w)) or (except9.match(w)):
                w = w + "ΕΤ"

        # Step 5d
        pattern = re.compile(r"^(.+?)(ΟΝΤΑΣ|ΩΝΤΑΣ)$")
        if pattern.match(w):
            fp = pattern.match(w).groups()
            stem = fp[0]
            w = stem
            test1 = False
            except10 = re.compile(r"^(ΑΡΧ)$")
            except11 = re.compile(r"(ΚΡΕ)$")
            if except10.match(w):
                w = w + "ΟΝΤ"
            if except11.match(w):
                w = w + "ΩΝΤ"

        # Step 5e
        pattern = re.compile(r"^(.+?)(ΟΜΑΣΤΕ|ΙΟΜΑΣΤΕ)$")
        if pattern.match(w):
            fp = pattern.match(w).groups()
            stem = fp[0]
            w = stem
            test1 = False
            except11 = re.compile("^(ΟΝ)$")
            if except11.match(w):
                w = w + "ΟΜΑΣΤ"

        # Step 5f
        pattern = re.compile(r"^(.+?)(ΕΣΤΕ)$")
        pattern2 = re.compile(r"^(.+?)(ΙΕΣΤΕ)$")
        if pattern2.match(w):
            fp = pattern2.match(w).groups()
            stem = fp[0]
            w = stem
            test1 = False
            pattern2 = re.compile(r"^(Π|ΑΠ|ΣΥΜΠ|ΑΣΥΜΠ|ΑΚΑΤΑΠ|ΑΜΕΤΑΜΦ)$")
            if pattern2.match(w):
                w = w + "ΙΕΣΤ"

        if pattern.match(w):
            fp = pattern.match(w).groups()
            stem = fp[0]
            w = stem
            test1 = False
            except12 = re.compile(r"^(ΑΛ|ΑΡ|ΕΚΤΕΛ|Ζ|Μ|Ξ|ΠΑΡΑΚΑΛ|ΑΡ|ΠΡΟ|ΝΙΣ)$")
            if except12.match(w):
                w = w + "ΕΣΤ"

        # Step 5g
        pattern = re.compile(r"^(.+?)(ΗΚΑ|ΗΚΕΣ|ΗΚΕ)$")
        pattern2 = re.compile(r"^(.+?)(ΗΘΗΚΑ|ΗΘΗΚΕΣ|ΗΘΗΚΕ)$")
        if pattern2.match(w):
            fp = pattern2.match(w).groups()
            stem = fp[0]
            w = stem
            test1 = False

        if pattern.match(w):
            fp = pattern.match(w).groups()
            stem = fp[0]
            w = stem
            test1 = False
            except13 = re.compile(r"(ΣΚΩΛ|ΣΚΟΥΛ|ΝΑΡΘ|ΣΦ|ΟΘ|ΠΙΘ)$")
            except14 = re.compile(r"^(ΔΙΑΘ|Θ|ΠΑΡΑΚΑΤΑΘ|ΠΡΟΣΘ|ΣΥΝΘ|)$")
            if (except13.match(w)) or (except14.match(w)):
                w = w + "ΗΚ"

        # Step 5h
        pattern = re.compile(r"^(.+?)(ΟΥΣΑ|ΟΥΣΕΣ|ΟΥΣΕ)$")
        if pattern.match(w):
            fp = pattern.match(w).groups()
            stem = fp[0]
            w = stem
            test1 = False
            except15 = re.compile(
                r"^(ΦΑΡΜΑΚ|ΧΑΔ|ΑΓΚ|ΑΝΑΡΡ|ΒΡΟΜ|ΕΚΛΙΠ|ΛΑΜΠΙΔ|ΛΕΧ|Μ|ΠΑΤ|Ρ|Λ|ΜΕΔ|ΜΕΣΑΖ|ΥΠΟΤΕΙΝ|ΑΜ|ΑΙΘ|ΑΝΗΚ|ΔΕΣΠΟΖ|ΕΝΔΙΑΦΕΡ|ΔΕ|ΔΕΥΤΕΡΕΥ|ΚΑΘΑΡΕΥ|ΠΛΕ|ΤΣΑ)$")
            except16 = re.compile(r"(ΠΟΔΑΡ|ΒΛΕΠ|ΠΑΝΤΑΧ|ΦΡΥΔ|ΜΑΝΤΙΛ|ΜΑΛΛ|ΚΥΜΑΤ|ΛΑΧ|ΛΗΓ|ΦΑΓ|ΟΜ|ΠΡΩΤ)$")
            if (except15.match(w)) or (except16.match(w)):
                w = w + "ΟΥΣ"

        # Step 5i
        pattern = re.compile(r"^(.+?)(ΑΓΑ|ΑΓΕΣ|ΑΓΕ)$")
        if pattern.match(w):
            fp = pattern.match(w).groups()
            stem = fp[0]
            w = stem
            test1 = False
            except17 = re.compile(r"^(ΨΟΦ|ΝΑΥΛΟΧ)$")
            except20 = re.compile(r"(ΚΟΛΛ)$")
            except18 = re.compile(
                r"^(ΑΒΑΣΤ|ΠΟΛΥΦ|ΑΔΗΦ|ΠΑΜΦ|Ρ|ΑΣΠ|ΑΦ|ΑΜΑΛ|ΑΜΑΛΛΙ|ΑΝΥΣΤ|ΑΠΕΡ|ΑΣΠΑΡ|ΑΧΑΡ|ΔΕΡΒΕΝ|ΔΡΟΣΟΠ|ΞΕΦ|ΝΕΟΠ|ΝΟΜΟΤ|ΟΛΟΠ|ΟΜΟΤ|ΠΡΟΣΤ|ΠΡΟΣΩΠΟΠ|ΣΥΜΠ|ΣΥΝΤ|Τ|ΥΠΟΤ|ΧΑΡ|ΑΕΙΠ|ΑΙΜΟΣΤ|ΑΝΥΠ|ΑΠΟΤ|ΑΡΤΙΠ|ΔΙΑΤ|ΕΝ|ΕΠΙΤ|ΚΡΟΚΑΛΟΠ|ΣΙΔΗΡΟΠ|Λ|ΝΑΥ|ΟΥΛΑΜ|ΟΥΡ|Π|ΤΡ|Μ)$")
            except19 = re.compile(r"(ΟΦ|ΠΕΛ|ΧΟΡΤ|ΛΛ|ΣΦ|ΡΠ|ΦΡ|ΠΡ|ΛΟΧ|ΣΜΗΝ)$")
            if (except18.match(w) and except19.match(w)) and not ((except17.match(w)) or (except20.match(w))):
                w = w + "ΑΓ"

        # Step 5j
        pattern = re.compile("^(.+?)(ΗΣΕ|ΗΣΟΥ|ΗΣΑ)$")
        if pattern.match(w):
            fp = pattern.match(w).groups()
            stem = fp[0]
            w = stem
            test1 = False
            except21 = re.compile(r"^(Ν|ΧΕΡΣΟΝ|ΔΩΔΕΚΑΝ|ΕΡΗΜΟΝ|ΜΕΓΑΛΟΝ|ΕΠΤΑΝ)$")
            if except21.match(w):
                w = w + "ΗΣ"

        # Step 5k
        pattern = re.compile(r"^(.+?)(ΗΣΤΕ)$")

        if pattern.match(w):
            fp = pattern.match(w).groups()
            stem = fp[0]
            w = stem
            test1 = False
            except22 = re.compile(r"^(ΑΣΒ|ΣΒ|ΑΧΡ|ΧΡ|ΑΠΛ|ΑΕΙΜΝ|ΔΥΣΧΡ|ΕΥΧΡ|ΚΟΙΝΟΧΡ|ΠΑΛΙΜΨ)$")
            if except22.match(w):
                w = w + "ΗΣΤ"

        # Step 5l
        pattern = re.compile("^(.+?)(ΟΥΝΕ|ΗΣΟΥΝΕ|ΗΘΟΥΝΕ)$")
        if pattern.match(w):
            fp = pattern.match(w).groups()
            stem = fp[0]
            w = stem
            test1 = False
            except23 = re.compile("^(Ν|Ρ|ΣΠΙ|ΣΤΡΑΒΟΜΟΥΤΣ|ΚΑΚΟΜΟΥΤΣ|ΕΞΩΝ)$")
            if except23.match(w):
                w = w + "ΟΥΝ"

        # Step 5l
        pattern = re.compile(r"^(.+?)(ΟΥΜΕ|ΗΣΟΥΜΕ|ΗΘΟΥΜΕ)$")
        if pattern.match(w):
            fp = pattern.match(w).groups()
            stem = fp[0]
            w = stem
            test1 = False
            except24 = re.compile(r"^(ΠΑΡΑΣΟΥΣ|Φ|Χ|ΩΡΙΟΠΛ|ΑΖ|ΑΛΛΟΣΟΥΣ|ΑΣΟΥΣ)$")
            if except24.match(w):
                w = w + "ΟΥΜ"

        # Step 6
        pattern = re.compile(r"^(.+?)(ΜΑΤΑ|ΜΑΤΩΝ|ΜΑΤΟΣ)$")
        pattern2 = re.compile(
            r"^(.+?)(Α|ΑΓΑΤΕ|ΑΓΑΝ|ΑΕΙ|ΑΜΑΙ|ΑΝ|ΑΣ|ΑΣΑΙ|ΑΤΑΙ|ΑΩ|Ε|ΕΙ|ΕΙΣ|ΕΙΤΕ|ΕΣΑΙ|ΕΣ|ΕΤΑΙ|Ι|ΙΕΜΑΙ|ΙΕΜΑΣΤΕ|ΙΕΤΑΙ|ΙΕΣΑΙ|ΙΕΣΑΣΤΕ|ΙΟΜΑΣΤΑΝ|ΙΟΜΟΥΝ|ΙΟΜΟΥΝΑ|ΙΟΝΤΑΝ|ΙΟΝΤΟΥΣΑΝ|ΙΟΣΑΣΤΑΝ|ΙΟΣΑΣΤΕ|ΙΟΣΟΥΝ|ΙΟΣΟΥΝΑ|ΙΟΤΑΝ|ΙΟΥΜΑ|ΙΟΥΜΑΣΤΕ|ΙΟΥΝΤΑΙ|ΙΟΥΝΤΑΝ|Η|ΗΔΕΣ|ΗΔΩΝ|ΗΘΕΙ|ΗΘΕΙΣ|ΗΘΕΙΤΕ|ΗΘΗΚΑΤΕ|ΗΘΗΚΑΝ|ΗΘΟΥΝ|ΗΘΩ|ΗΚΑΤΕ|ΗΚΑΝ|ΗΣ|ΗΣΑΝ|ΗΣΑΤΕ|ΗΣΕΙ|ΗΣΕΣ|ΗΣΟΥΝ|ΗΣΩ|Ο|ΟΙ|ΟΜΑΙ|ΟΜΑΣΤΑΝ|ΟΜΟΥΝ|ΟΜΟΥΝΑ|ΟΝΤΑΙ|ΟΝΤΑΝ|ΟΝΤΟΥΣΑΝ|ΟΣ|ΟΣΑΣΤΑΝ|ΟΣΑΣΤΕ|ΟΣΟΥΝ|ΟΣΟΥΝΑ|ΟΤΑΝ|ΟΥ|ΟΥΜΑΙ|ΟΥΜΑΣΤΕ|ΟΥΝ|ΟΥΝΤΑΙ|ΟΥΝΤΑΝ|ΟΥΣ|ΟΥΣΑΝ|ΟΥΣΑΤΕ|Υ|ΥΣ|Ω|ΩΝ)$")

        if pattern.match(w):
            fp = pattern.match(w).groups()
            stem = fp[0]
            w = stem + "ΜΑ"

        if pattern2.match(w) and test1:
            fp = pattern2.match(w).groups()
            stem = fp[0]
            w = stem

        # Step 7 (ΠΑΡΑΘΕΤΙΚΑ)
        pattern = re.compile(r"^(.+?)(ΕΣΤΕΡ|ΕΣΤΑΤ|ΟΤΕΡ|ΟΤΑΤ|ΥΤΕΡ|ΥΤΑΤ|ΩΤΕΡ|ΩΤΑΤ)$")
        if pattern.match(w):
            fp = pattern.match(w).groups()
            stem = fp[0]
            w = stem

        return w
