# Compiler Design

Comprehensive compilation of Previous Year Questions (PYQs) for **Compiler Design (CS 4101)** covering the years **2025, 2024, and 2023** from IIEST Shibpur examinations.

---

## Contents

- [2025 Examinations](#2025-examinations)
  - [2025 Mid-Semester Examination (September 2025)](#2025-mid-semester-examination-september-2025)
  - [2025 End-Semester Examination (November 2025)](#2025-end-semester-examination-november-2025)
- [2024 Examinations](#2024-examinations)
  - [2024 Mid-Semester Examination (September 2024)](#2024-mid-semester-examination-september-2024)
  - [2024 End-Semester Examination (November 2024)](#2024-end-semester-examination-november-2024)
- [2023 Examinations](#2023-examinations)
  - [2023 Mid-Semester Examination (September 2023)](#2023-mid-semester-examination-september-2023)
  - [2023 End-Semester Examination (November 2023)](#2023-end-semester-examination-november-2023)

---

## 2025 Examinations

### 2025 Mid-Semester Examination (September 2025)

**Indian Institute of Engineering Science and Technology, Shibpur**  
**B.Tech. - M.Tech. Dual Degree $7^{\text{th}}$ Mid-Semester (CST) Examination, September 2025**  
**Compiler Design (CS 4101)**  
**Full Marks: 30 · Time: 2 Hours**  
*Answer Question-1 and any three from the remaining.*

1. **(a)** What advantages are there to a language-processing system in which the compiler produces assembly language rather than machine language?  
   **(b)** Explain tokens, patterns, and lexemes. Demonstrate the same with examples. **[3 + 3 = 6]**

2. **(a)** Write regular expressions for specifying identifiers and constants of C. Discuss how finite automata is used to represent tokens and performs lexical analysis with examples.  
   **(b)** Consider the following Context Free Grammar where $S$ is the start symbol:
   
   $$S \to SS + \mid SS * \mid a$$
   
   and the string $aa + a*$.  
   i. Give the leftmost derivation of the string.  
   ii. Give rightmost derivation of the string.  
   iii. Give the parse tree of the string.  
   iv. Is the grammar ambiguous or unambiguous? Justify your answer. **[4 + 4 = 8]**

3. Consider the following Grammar, $G = (\{A, B\}, \{a, b, c, d\}, P, A)$ where $P$ is the set of production rules as follows:
   
   $$
   \begin{aligned}
   A &\to Aa \mid Aab \mid Bc \\
   B &\to BAa \mid d
   \end{aligned}
   $$
   
   **(a)** Eliminate left recursion from the above grammar.  
   **(b)** Compute FIRST & FOLLOW set for the non-terminals. Check the grammar is LL(1) or not; Show the parsing for $dcab$. **[2 + 6 = 8]**

4. **(a)** What are the use of shift reduces parser? Explain conflicts that may occur during shift-reduce parsing.  
   **(b)** What do you mean by handle pruning in bottom-up parsing? Explain with the help of the grammar $S \to SS + \mid SS * \mid a$ and input string $aaa*a++$. In each reduction indicate the corresponding handle. **[3 + 5 = 8]**

5. Check whether the following grammar is SLR(1) or not. Explain your answer with Reasons:
   
   $$
   \begin{aligned}
   S &\to L = R \\
   S &\to R \\
   L &\to *R \\
   L &\to id \\
   R &\to L
   \end{aligned}
   $$
   
   **[5 + 3 = 8]**

---

### 2025 End-Semester Examination (November 2025)

**Indian Institute of Engineering Science and Technology, Shibpur**  
**Dual Degree (B.Tech. - M.Tech.) $7^{\text{th}}$ Semester (CST) Examination, November 2025**  
**Compiler Design (CS 4101)**  
**Full Marks: 50 · Time: 3 Hours**  
*Answer Question-1 and any four from the remaining.*

1. **(a)** Explain the error handling and error recovery mechanism of syntax analyser. **[4]**  
   **(b)** Explain the following peephole optimization techniques:
   - a) Elimination of Redundant Code
   - b) Elimination of Unreachable Code **[1 + 1 = 2]**

2. **(a)** Consider the following Context Free Grammar where $S$ is the start symbol:
   
   $$
   \begin{aligned}
   S &\to L = R \\
   S &\to R \\
   L &\to *R \\
   L &\to id \\
   R &\to L
   \end{aligned}
   $$
   
   Check whether the grammar is ambiguous or not.  
   **(b)** What is recursive descent parsing? List the problems faced in designing such a parser.  
   **(c)** Construct a Finite Automata equivalent to the regular expression:
   
   $$(0 + 1)^*(00 + 11)(0 + 1)^*$$
   
   **[4 + 4 + 3 = 11]**

3. Consider the following grammar production rules where $S$ is the start symbol:
   
   $$
   \begin{aligned}
   S &\to ABD \\
   A &\to a \mid DB \mid \varepsilon \\
   B &\to gD \mid dA \mid \varepsilon \\
   D &\to e \mid f
   \end{aligned}
   $$
   
   **(a)** Construct FIRST and FOLLOW for each non-terminal of the above grammar.  
   **(b)** Construct the predictive parsing table for the above grammar.  
   **(c)** Show the parsing on a valid string and on an invalid string.  
   **(d)** Check whether the grammar is LL(1). Give justification. **[3 + 3 + 3 + 2 = 11]**

4. **(a)** Explain the model of shift reduces parser? Explain conflicts that may occur during shift-reduce parsing.  
   **(b)** Construct the CLR parsing table for the following grammar where $S$ is the start symbol:
   
   $$
   \begin{aligned}
   S &\to CC \\
   C &\to cC \mid d \mid \varepsilon
   \end{aligned}
   $$
   
   **[5 + 6 = 11]**

5. **(a)** Write down the algorithm to find the leader in basic block. Write down the three-address code and construct the basic blocks for the following program segment:
   
   ```c
   sum = 0;
   i = 0;
   while (i <= 10)
   {
       sum = sum + a[i];
       i++;
   }
   ```
   
   where the datatype for $a$, $b$ and $x$ are integer.  
   **(b)** Why symbol-table is needed in various phases of compilers? How hashing can be used to design symbol-table?  
   **(c)** Explain the characteristics of peephole code optimization technique. **[3 + 5 + 3 = 11]**

6. **(a)** Explain the simplification of simple type checker for statements, expressions and functions. **[6]**  
   **(b)** Explain Loop optimization in detail using suitable example. **[5]** **[6 + 5 = 11]**

7. **(a)** Explain the sequence of the stack allocation process for a function call using a suitable example.  
   **(b)** Translate the expression $-(a+b)*(c+d)+(a+b+c)$ into: (i) quadruples, (ii) triples and (iii) indirect triples.  
   **(c)** Define the activation record. What are the contents of activation record? **[3 + 5 + 3 = 11]**

---

## 2024 Examinations

### 2024 Mid-Semester Examination (September 2024)

**Indian Institute of Engineering Science and Technology, Shibpur**  
**B.Tech. - M.Tech. Dual Degree $7^{\text{th}}$ Mid-Semester (CST) Examination, September 2024**  
**Compiler Design (CS 4101)**  
**Full Marks: 30 · Time: 2 Hours**  
*Answer Question-1 and any three from the remaining.*

1. **(a)** List out the functions of a Lexical Analyzer. State the reasons for the separation of Analysis programs into Lexical, Syntax, and Semantic Analyses.  
   **(b)** Explain the various errors encountered in different phases of compiler. **[3 + 3 = 6]**

2. **(a)** Write regular expressions for specifying identifiers and constants of C. Discuss how finite automata is used to represent tokens and performs lexical analysis with examples.  
   **(b)** Explain panic mode error recovery strategy for predictive parsing method using a suitable example. **[4 + 4 = 8]**

3. Consider the following Grammar production rules where $E$ is the start symbol:
   
   $$
   \begin{aligned}
   E &\to E + T \mid T \\
   T &\to TF \mid F \\
   F &\to F* \mid a \mid b
   \end{aligned}
   $$
   
   **(a)** Eliminate left recursion from the above grammar.  
   **(b)** Compute FIRST & FOLLOW set for the non-terminals. Check the grammar is LL(1) or not; Show the parsing for $a + a + a$. **[2 + 6 = 8]**

4. **(a)** What are the use of shift reduces parser? Explain conflicts that may occur during shift-reduce parsing.  
   **(b)** What do you mean by handle pruning in bottom-up parsing? Explain with the help of the grammar $S \to SS + \mid SS * \mid a$ and input string $aaa*a++$. In each reduction indicate the corresponding handle. **[3 + 5 = 8]**

5. What is LALR(1) grammar? Construct LALR parsing table for the following grammar:
   
   $$
   \begin{aligned}
   S &\to CC \\
   C &\to cC \\
   C &\to c \mid d
   \end{aligned}
   $$
   
   **[3 + 5 = 8]**

---

### 2024 End-Semester Examination (November 2024)

**Indian Institute of Engineering Science and Technology, Shibpur**  
**Dual Degree (B.Tech. - M.Tech.) $7^{\text{th}}$ Semester (CST) Examination, November 2024**  
**Compiler Design (CS 4101)**  
**Full Marks: 50 · Time: 3 Hours**  
*Answer Question-1 and any four from the remaining.*

1. **(a)** Describe hash-table based data structures for symbol table management.  
   **(b)** Write the regular expressions to describe languages consisting of strings made of even numbers of $a$ and $b$. **[3 + 3 = 6]**

2. **(a)** What is meant by lexical analysis? Identify the lexemes that make up the token in the following program segment. Indicate the corresponding token and pattern:
   
   ```c
   void swap(int i, int j)
   {
       int t;
       t = i;
       i = j;
       j = t;
   }
   ```
   
   **(b)** Draw the transition diagram for relational operators and unsigned numbers. **[4 + (4 + 3) = 11]**

3. Consider the following grammar production rules where $S$ is the start symbol:
   
   $$
   \begin{aligned}
   E &\to E + T \mid T \\
   T &\to TF \mid F \\
   F &\to F* \mid a \mid b
   \end{aligned}
   $$
   
   **(a)** Write the rules to eliminate left recursion in a grammar. Eliminate left recursion from the above grammar.  
   **(b)** Compute FIRST & FOLLOW set for the non-terminals. Check the grammar is LL(1) or not; Show the parsing for $a + b + a$. **[3 + (4 + 1 + 3) = 11]**

4. **(a)** Explain the model of shift reduces parser? Explain conflicts that may occur during shift-reduce parsing.  
   **(b)** Construct the CLR parsing table for the following grammar where $S$ is the start symbol:
   
   $$
   \begin{aligned}
   S &\to CC \\
   C &\to cC \mid d \mid \varepsilon
   \end{aligned}
   $$
   
   **[5 + 6 = 11]**

5. **(a)** Describe the evaluation order of Syntax Directed Translation (SDT) with an example.  
   **(b)** Generate intermediate code for the following code segment along with the required syntax directed definition:
   
   ```c
   if (a > b)
       x = a + b;
   else
       x = a - b;
   ```
   
   Here datatype for $x$, $a$ and $b$ are int. **[6 + 5 = 11]**

6. **(a)** Discuss the following: (i) Dead code elimination and (ii) copy propagation.  
   **(b)** Construct the DAG for the following sequence of codes:
   
   ```text
   1.  t1 := 4 * i
   2.  t2 := a[t1]
   3.  t3 := 4 * i
   4.  t4 := b[t3]
   5.  t5 := t2 * t4
   6.  t6 := prod + t5
   7.  prod := t6
   8.  t7 := i + 1
   9.  i := t7
   10. if i <= 20 goto 1
   ```
   
   **(c)** Explain loop optimization in detail using a suitable example. **[4 + 3 + 4 = 11]**

7. **(a)** Explain the sequence of the stack allocation process for a function call using a suitable example.  
   **(b)** Translate the expression $-(a+b)*(c+d)+(a+b+c)$ into: (i) quadruples, (ii) triples and (iii) indirect triples.  
   **(c)** Define the activation record. What are the contents of activation record? **[3 + 5 + 3 = 11]**

---

## 2023 Examinations

### 2023 Mid-Semester Examination (September 2023)

**Indian Institute of Engineering Science and Technology, Shibpur**  
**B.Tech. - M.Tech. Dual Degree $7^{\text{th}}$ Semester (CST) Examination (Mid Semester) 2023**  
**Compiler Design (CS 4101)**  
**Full Marks: 30 · Time: 2 Hours**  
*Answer Question-1 and any three from the remaining. Do all parts of a question together. Do not mix up answers to parts of different questions in the answer script.*

1. **(a)** List out the functions of a Lexical Analyzer. State the reasons for the separation of Analysis programs into Lexical, Syntax, and Semantic Analyses.  
   **(b)** Explain the various errors encountered in different phases of compiler. **[3 + 3 = 6]**

2. **(a)** Discuss how finite automata is used to represent tokens and performs lexical analysis with examples.  
   **(b)** Explain panic mode error recovery strategy for predictive parsing method using a suitable example. **[4 + 4 = 8]**

3. Consider the following Grammar production rules where $E$ is the start symbol:
   
   $$
   \begin{aligned}
   E &\to E + T \mid T \\
   T &\to TF \mid F \\
   F &\to F* \mid a \mid b
   \end{aligned}
   $$
   
   **(a)** Eliminate left recursion from the above grammar.  
   **(b)** Compute FIRST & FOLLOW set for the non-terminals. Check the grammar is LL(1) or not; Show the parsing for $a + a + a$. **[2 + 6 = 8]**

4. **(a)** What are the use of shift reduces parser? Explain conflicts that may occur during shift-reduce parsing.  
   **(b)** What do you mean by handle pruning in bottom-up parsing? Explain with the help of the grammar $S \to SS + \mid SS * \mid a$ and input string $aaa*a++$. In each reduction indicate the corresponding handle. **[3 + 5 = 8]**

5. Construct the SLR sets of items for the grammar where $E$ is the start symbol:
   
   $$
   \begin{aligned}
   E &\to E + T \mid T \\
   T &\to TF \mid F \\
   F &\to F* \mid a \mid b
   \end{aligned}
   $$
   
   Show the SLR parsing table for this grammar. Is the grammar SLR? **[5 + 3 = 8]**

---

### 2023 End-Semester Examination (November 2023)

**Indian Institute of Engineering Science and Technology, Shibpur**  
**Dual Degree (B.Tech.-M.Tech.) $7^{\text{th}}$ Semester (CST) Examination (End Semester) November, 2023**  
**Compiler Design (CS 4101)**  
**Full Marks: 50 · Time: 3 Hours**  
*Answer Question-1 and any four from the remaining. Do all parts of a question together. Do not mix up answers to parts of different questions in the answer script.*

1. **(a)** Write regular expressions to specify the identifiers and constants of C.  
   **(b)** What do you mean by left factoring of grammar? Explain.  
   **(c)** What is a handle in bottom up parsing? Explain. **[2 + 2 + 2 = 6]**

2. Consider the following Grammar production rules where $S$ is the start symbol:
   
   $$
   \begin{aligned}
   S &\to ACB \mid CbB \mid Ba \\
   A &\to da \mid BC \\
   B &\to g \mid \varepsilon \\
   C &\to h \mid \varepsilon
   \end{aligned}
   $$
   
   **(a)** Eliminate left recursion from the above grammar.  
   **(b)** Compute FIRST & FOLLOW set for the non-terminals. Check the grammar is LL(1) or not; Show the parsing for "ghhg". **[3 + (4 + 1 + 3) = 11]**

3. **(a)** Explain the model of shift reduces parser? Explain conflicts that may occur during shift-reduce parsing.  
   **(b)** Construct the CLR parsing table for the following grammar where $S$ is the start symbol:
   
   $$
   \begin{aligned}
   S &\to L = R \mid R \\
   L &\to *R \mid id \\
   R &\to L
   \end{aligned}
   $$
   
   **[5 + 6 = 11]**

4. **(a)** Explain the use of symbol table in compilation process. List out the various attributes for implementing the symbol table.  
   **(b)** Generate intermediate code for the following code segment along with the required syntax directed definition:
   
   ```c
   if (a > b)
       x = a + b;
   else
       x = a - b;
   ```
   
   Here datatype for $x$, $a$ and $b$ are int. **[6 + 5 = 11]**

5. **(a)** Explain the algebraic translations of local machine-independent optimizations.  
   **(b)** Discuss the following: (i) Dead code elimination and (ii) copy propagation.  
   **(c)** Explain loop optimization in detail using a suitable example. **[3 + 4 + 4 = 11]**

6. **(a)** Translate the expression $-(a+b)*(c+d)+(a+b+c)$ into: (i) quadruples, (ii) triples and (iii) indirect triples.  
   **(b)** List the fields in an activation record. Write down the purpose of each of these fields in an activation record.  
   **(c)** Explain the sequence of stack allocation process for a function call using suitable example. **[3 + 5 + 3 = 11]**
