# Proofing corrections applied to the Georgian thesis

63 verified find-replace corrections (from the coherence review), applied deterministically in build.py via corrections.json. Each was checked: exact source count, zero residual after apply, no collateral. Grouped below for author review — flag any you disagree with.

## 1. Meaning-reversing mistranslations
- «წოდებული "სათადარიგო"» → «წოდებული „კომპანიონი“»  
  _MEANING: companion (not spare). §1.1_
- «არც გახანგრძლივება, არც» → «არც დაქრობა, არც»  
  _MEANING: decay (not prolongation). §1.2 triad_
- «დამოკიდებულ გახანგრძლივებას» → «დამოკიდებულ დაქრობას»  
  _MEANING: decay. §2.2_
- «გახანგრძლივება, სალიენცობა» → «დაქრობა, სალიენცობა»  
  _MEANING: decay. §4.3 triad_
- «ენერგეტიკული ანალიზით» → «ძალის (სტატისტიკური სიმძლავრის) ანალიზით»  
  _MEANING: statistical power analysis (not energy). §3.1_
- «საშუალო ტურნირის» → «საშუალო ტურის»  
  _MEANING: per-turn (not tournament). §3.2_
- «ინფორმაციის გამოსათვლელად» → «ინფორმაციის გასახსენებლად»  
  _MEANING: cross-session recall (not calculation). §5.2_
- «უსასრულო დაქვეითება» → «ზარმაცი დაქვეითება»  
  _MEANING: lazy decay (not infinite). §3.4_
- «ცოდნილ რეალიზმს» → «კოგნიტურ რეალიზმს»  
  _MEANING: cognitive realism (not 'known'). §3.8_
- «თავის ხუთი საწყისი თეორიას აერთიანებდა კი არ, არამედ ქმნიდა მათგან ახალს» → «თავის ხუთ საწყის თეორიას კომპოზიციად აწყობს და არა ერთ მთლიანობად აერთიანებს»  
  _MEANING: composes rather than unifies (was 'created something new'). §3.8 — INTERPRETIVE, author confirm verb_
- «ჩამორჩენილი კომენტარი» → «გაკვრით ნათქვამი კომენტარი»  
  _MEANING: passing remark (not 'backward'). §4.1_
- «სიხშირული ფილტრის» → «სალიენს-გეითინგის»  
  _MEANING: salience-gating (not 'frequency filter'). §3.3_

## 2. Broken/garbled words & characters
- «დაუჯერღვანელებელ» → «დაუმუშავებელ»  
  _NON-WORD: undigested → unprocessed. §2.2_
- «უსხვამისეულად» → «განურჩევლად»  
  _NON-WORD: indiscriminately. §4.2_
- «ხმის პიპელა» → «ხმის მილსადენი»  
  _NON-WORD: pipeline. §4.1 (Table 4.1)_
- «ზოგადყოფების» → «განზოგადებების»  
  _NON-WORD: generalizations. §3.2_
- «გასამოსაჯაროებელი» → «გამოსაქვეყნებელი»  
  _NON-WORD: publishable. §3.1_
- «ნაწინდევრებული» → «პროგნოზირებული»  
  _GARBLED: predicted. §1.2_
- «(გიუსტი)» → «(gist)»  
  _NON-WORD gloss. §2.2_
- «კომპრესიя» → «კომპრესია»  
  _CYRILLIC я (U+044F) → Georgian ა. Table 3.1_

## 3. Number errors
- «თვრამეტ კონსტრუქტს» → «ცხრამეტ კონსტრუქტს»  
  _NUMBER: ASAQ 19 constructs (not 18). §2.6_
- «თვრამეტი ცხრა კონსტრუქტს» → «ცხრამეტ კონსტრუქტს»  
  _NUMBER: garbled '18 9' → 19. §3.6_

## 4. Terminology consistency (glossary)
- «სოციალური თანადგომა» → «სოციალური თანდასწრება»  
  _TERM social presence. Nominative_
- «სოციალურ თანადგომაზე» → «სოციალურ თანდასწრებაზე»  
  _TERM social presence. -ზე_
- «სოციალურ თანადგომას» → «სოციალურ თანდასწრებას»  
  _TERM social presence. Dative_
- «სოციალური თანადგომის» → «სოციალური თანდასწრების»  
  _TERM social presence. Genitive_
- «სოციალური პრეზენციისა» → «სოციალური თანდასწრებისა»  
  _TERM social presence (presence variant). Genitive_
- «სოციალურ პრეზენციას» → «სოციალურ თანდასწრებას»  
  _TERM social presence (presence variant). Dative_
- «დავიწყების კრუგი,» → «დავიწყების მრუდი,»  
  _TERM forgetting curve (Rus. круг). Nom, comma-bounded_
- «დავიწყების კრუგი.» → «დავიწყების მრუდი.»  
  _TERM forgetting curve. Nom, period-bounded_
- «დავიწყების კრუგს» → «დავიწყების მრუდს»  
  _TERM forgetting curve. Dative_
- «დავიწყების კრუგისთვის» → «დავიწყების მრუდისთვის»  
  _TERM forgetting curve. Gen+postp_
- «დავიწყების კურივა» → «დავიწყების მრუდი»  
  _TERM forgetting curve (Rus. кривая). §2.4_
- «ლატენტურობისა» → «დაყოვნებისა»  
  _TERM latency (glossary). Gen+euphonic_
- «ლატენტურობა» → «დაყოვნება»  
  _TERM latency. Nominative_
- «კონფუუდის» → «აღრევის ფაქტორის»  
  _TERM confound. Genitive_
- «წაკითხვადობის კონფუუდი» → «წაკითხვადობის აღრევის ფაქტორი»  
  _TERM confound. Nom, bounded_
- «ამ კონფუუდს» → «ამ აღრევის ფაქტორს»  
  _TERM confound. Dative, bounded_
- «კონფუუნდების» → «აღრევის ფაქტორების»  
  _TERM confound (misspelling). Gen pl_
- «თანაშემწისგან» → «ასისტენტისგან»  
  _TERM assistant. §1.5_
- «თანაშემწიდან» → «ასისტენტიდან»  
  _TERM assistant. §5_
- «დამხმარედან» → «ასისტენტიდან»  
  _TERM assistant. §2.6 heading_
- «დამხმარისგან» → «ასისტენტისგან»  
  _TERM assistant. §2.6_
- «საუბრის პარტნიორის» → «თანამოსაუბრის»  
  _TERM interlocutor. Genitive_
- «საუბრის პარტნიორს» → «თანამოსაუბრეს»  
  _TERM interlocutor. Dative_
- «აღჭურვილი საუბრის პარტნიორი» → «აღჭურვილი თანამოსაუბრე»  
  _TERM interlocutor. Nom, bounded_
- «ადამიანი-საუბრის პარტნიორი» → «ადამიანი-თანამოსაუბრე»  
  _TERM interlocutor. Nom, bounded_
- «საუბრის პარტნიორი მდგრადად» → «თანამოსაუბრე მდგრადად»  
  _TERM interlocutor. Nom, bounded_
- «საუბრის პარტნიორი გადადის» → «თანამოსაუბრე გადადის»  
  _TERM interlocutor. Nom, bounded_
- «ინტერლოკუტორი» → «თანამოსაუბრე»  
  _TERM interlocutor (translit). Nom_
- «ინტერლოკუტორს» → «თანამოსაუბრეს»  
  _TERM interlocutor. Dative_
- «მრავალსაცავო მოდელი» → «მრავალსაცავიანი მოდელი»  
  _TERM multi-store model. Nominative_
- «მრავალსაცავო მოდელს» → «მრავალსაცავიან მოდელს»  
  _TERM multi-store model. Dative_
- «მრავალსაწყობიანი» → «მრავალსაცავიანი»  
  _TERM multi-store model (variant). Nominative_
- «ებინგჰაუზ» → «ებინგჰაუს»  
  _PROPER NAME: Ebbinghaus ზ→ს (glossary). Stem, all endings_
- «ქცევითი ხელწერა» → «ქცევითი სიგნატურა»  
  _TERM behavioral signature. Nominative_
- «ქცევით ხელწერას» → «ქცევით სიგნატურას»  
  _TERM behavioral signature. Dative_
- «დუნე კვალითეორია» → «ბუნდოვანი კვალის თეორია»  
  _TERM fuzzy-trace (garbled). §2.2 heading_
- «ბურუსიანი კვალი» → «ბუნდოვანი კვალი»  
  _TERM fuzzy-trace ('misty trace'). §3.2_
- «კერძოობის კომფორტი» → «კონფიდენციალურობის კომფორტი»  
  _TERM (Table 4.3) privacy comfort_
- «შეფასებული ინტელექტი» → «აღქმული ინტელექტი»  
  _TERM (Table 4.3) perceived intelligence_
- «საინტერესო ფაქტები» → «წვრილმანები»  
  _TERM (Table 4.2 header) trivia_
- «დროში აზროვნებისას» → «დროითი (ტემპორალური) მსჯელობისას»  
  _TERM temporal reasoning. Abstract_

## Deferred (author decision — NOT changed)
- §2.6 «დამხმარე საპილოტე კვლევა» — here «დამხმარე» = *auxiliary* (adj. modifying "pilot study"), not the assistant role; left as-is.
- Stage-rubric field labels «ხელწერა:» (×5) — left as-is; change to «სიგნატურა:» if you want full consistency.
- «გისტი/საყრდენი» (P152) other gist transliteration — glossary term is «არსობრივი (gist)»; standardize if preferred.
- ASCII straight quotes throughout — glossary wants „…" ; only the companion term was converted. A global quote pass is optional.
- Interpretive verb in «composes rather than unifies» fix (აწყობს) — please confirm.