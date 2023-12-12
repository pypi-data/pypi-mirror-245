queue_using_array = '''
#include<stdio.h>
#include<conio.h>
#define SIZE 10

int queue[SIZE];
int front = -1, rear = -1;

void enqueue()
{
    if (rear >= SIZE - 1)
    {
        printf("Queue overflow\\n");
        return;
    }
    int data;
    printf("Enter data to be entered: ");
    scanf("%d", &data);
    if (front == -1)
        front = 0;
    rear++;
    queue[rear] = data;
    printf("%d added to queue\\n", data);
}

void dequeue()
{
    if (front == -1)
    {
        printf("Queue underflow\\n");
        return;
    }
    printf("%d removed from queue\\n", queue[front]);
    front++;
    if (front > rear)
        front = rear = -1;
}

void display()
{
    if (rear >= 0)
    {
        printf("Queue elements are:\\n");
        for (int i = front; i <= rear; i++){
            printf("%d  ", queue[i]);
        }
        printf("\\n");
    }
    else
    {
        printf("Queue is empty\\n");
    }
}

int main()
{
    int choice;
    do
    {
        printf("1. Enqueue\\n");
        printf("2. Dequeue\\n");
        printf("3. Display\\n");
        printf("4. Exit\\n");
        printf("Enter your choice: ");
        scanf("%d", &choice);
        switch (choice)
        {
        case 1:
            enqueue();
            break;
        case 2:
            dequeue();
            break;
        case 3:
            display();
            break;
        case 4:
            printf("Program Terminated.\\n");
            break;
        default:
            printf("Invalid choice.\\n");
        }
    } while (choice != 4);
}
'''

stack_using_array='''
// Implement stack using array
#include<stdio.h>
#include<conio.h>

#define SIZE 5
int stack[SIZE];
int top = -1;

void push(int val) {
	if (top == SIZE - 1) {
		printf("\\nStack overflow!\\n");
	}
	else {
		top++;
		stack[top] = val;
	}
}

int pop() {
	int x = -1;
	if (top == -1) {
		printf("\\nStack underflow\\n");
	}
	else {
		x = stack[top];
		top--;
	}
	return x;
}

int peek() {
	int x = -1;
	if (top == -1) {
		printf("\\nStack underflow\\n");
	}
	else {
		x = stack[top];
	}
	return x;
}

void display() {
	int i;
	if (top == -1)
		printf("\\nStack is empty\\n");
	else {
		for (i = top; i >= 0; i--) {
			printf("%d ", stack[i]);
		}
		printf("\\n");
	}
}

int main() {
	int choice, input, x;
	// clrscr();
	do {
		printf("1. Push\\n2. Pop\\n3. Peek\\n4. Display\\n5. Exit\\nEnter a choice: ");
		scanf("%d", &choice);
		switch (choice) {
			case 1:
				printf("\\nEnter the element to push: ");
				scanf("%d", &input);
				push(input);
				break;
			case 2:
				x = pop();
				if (x != -1)
					printf("\\nElement popped is %d\\n", x);
				break;
			case 3:
				x = peek();
				if (x != -1)
					printf("\\nElement at the top is %d\\n", x);
				break;
			case 4:
				printf("\\nThe stack currently is:\\n");
				display();
				break;
			case 5:
				break;
			default:
				printf("\\nInvalid choice!\tTry again later\\n");
				choice = 5;
		}
	} while (choice != 5);
	printf("\\nExited! Press any key to close\\n");
	// getch();
	return 0;
}
'''

linked_list='''
#include <stdio.h>
#include <stdlib.h>

struct Node {
    int data;
    struct Node* next;
};

void insert(struct Node** head, int data) {
    struct Node* newNode = (struct Node*)malloc(sizeof(struct Node));
    newNode->data = data;
    newNode->next = NULL;

    if (*head == NULL) {
        *head = newNode;
    } else {
        struct Node* current = *head;
        while (current->next != NULL) {
            current = current->next;
        }
        current->next = newNode;
    }
}

void removeNode(struct Node** head, int data) {
    struct Node* current = *head;
    struct Node* prev = NULL;

    while (current != NULL && current->data != data) {
        prev = current;
        current = current->next;
    }

    if (current == NULL) {
        printf("Element not found in the list.\\n");
        return;
    }

    if (prev == NULL) {
        *head = current->next;
    } else {
        prev->next = current->next;
    }

    free(current);
}


void display(struct Node* head) {
    struct Node* current = head;

    if (current == NULL) {
        printf("The list is empty.\\n");
        return;
    }

    printf("Linked List: ");
    while (current != NULL) {
        printf("%d -> ", current->data);
        current = current->next;
    }
    printf("NULL\\n");
}


int search(struct Node* head, int data) {
    struct Node* current = head;
    int position = 1;

    while (current != NULL) {
        if (current->data == data) {
            return position;
        }
        current = current->next;
        position++;
    }

    return -1; 
}

int main() {
    struct Node* head = NULL;
    int choice, data;

    while (1) {
        printf("\\nLinked List Operations:\\n");
        printf("1. Insert\\n");
        printf("2. Remove\\n");
        printf("3. Display\\n");
        printf("4. Search\\n");
        printf("5. Exit\\n");
        printf("Enter your choice: ");
        scanf("%d", &choice);

        switch (choice) {
            case 1:
                printf("Enter data to insert: ");
                scanf("%d", &data);
                insert(&head, data);
                break;
            case 2:
                printf("Enter data to remove: ");
                scanf("%d", &data);
                removeNode(&head, data);
                break;
            case 3:
                display(head);
                break;
            case 4:
                printf("Enter data to search: ");
                scanf("%d", &data);
                int position = search(head, data);
                if (position != -1) {
                    printf("Element found at position %d.\\n", position);
                } else {
                    printf("Element not found in the list.\\n");
                }
                break;
            case 5:
                exit(0);
            default:
                printf("Invalid choice. Please try again.\\n");
        }
    }

    return 0;
}

'''

polynomial_add_sub='''
#include <stdio.h>
#include <stdlib.h>

// Node structure to represent a term in a polynomial
typedef struct Node {
    int coefficient;
    int exponent;
    struct Node* next;
} Node;

// Function to create a new node
Node* createNode(int coef, int exp) {
    Node* newNode = (Node*)malloc(sizeof(Node));
    if (newNode == NULL) {
        printf("Memory allocation failed\\n");
        exit(1);
    }
    newNode->coefficient = coef;
    newNode->exponent = exp;
    newNode->next = NULL;
    return newNode;
}

// Function to insert a term into a polynomial (linked list)
void insertTerm(Node** poly, int coef, int exp) {
    Node* newNode = createNode(coef, exp);
    if (*poly == NULL) {
        *poly = newNode;
    } else {
        Node* current = *poly;
        while (current->next != NULL) {
            current = current->next;
        }
        current->next = newNode;
    }
}

// Function to display a polynomial
void displayPolynomial(Node* poly) {
    if (poly == NULL) {
        printf("Polynomial is empty\\n");
        return;
    }

    while (poly != NULL) {
        printf("%dx^%d ", poly->coefficient, poly->exponent);
        if (poly->next != NULL) {
            printf("+ ");
        }
        poly = poly->next;
    }
    printf("\\n");
}

// Function to add two polynomials
Node* addPolynomials(Node* poly1, Node* poly2) {
    Node* result = NULL;
    while (poly1 != NULL && poly2 != NULL) {
        if (poly1->exponent > poly2->exponent) {
            insertTerm(&result, poly1->coefficient, poly1->exponent);
            poly1 = poly1->next;
        } else if (poly1->exponent < poly2->exponent) {
            insertTerm(&result, poly2->coefficient, poly2->exponent);
            poly2 = poly2->next;
        } else {
            // Exponents are equal, add coefficients
            insertTerm(&result, poly1->coefficient + poly2->coefficient, poly1->exponent);
            poly1 = poly1->next;
            poly2 = poly2->next;
        }
    }

    // Add remaining terms from poly1
    while (poly1 != NULL) {
        insertTerm(&result, poly1->coefficient, poly1->exponent);
        poly1 = poly1->next;
    }

    // Add remaining terms from poly2
    while (poly2 != NULL) {
        insertTerm(&result, poly2->coefficient, poly2->exponent);
        poly2 = poly2->next;
    }

    return result;
}

// Function to subtract two polynomials
Node* subtractPolynomials(Node* poly1, Node* poly2) {
    // To subtract, we negate the coefficients of the second polynomial and then add
    Node* negPoly2 = NULL;
    while (poly2 != NULL) {
        insertTerm(&negPoly2, -poly2->coefficient, poly2->exponent);
        poly2 = poly2->next;
    }

    return addPolynomials(poly1, negPoly2);
}

// Function to free the memory used by a polynomial (linked list)
void freePolynomial(Node* poly) {
    Node* current = poly;
    Node* next;
    while (current != NULL) {
        next = current->next;
        free(current);
        current = next;
    }
}

int main() {
    int choice;
    Node* poly1 = NULL;
    Node* poly2 = NULL;

    do {
        printf("\\n1. Enter Polynomial 1\\n");
        printf("2. Enter Polynomial 2\\n");
        printf("3. Add Polynomials\\n");
        printf("4. Subtract Polynomials\\n");
        printf("5. Display Polynomials\\n");
        printf("6. Quit\\n");
        printf("Enter your choice: ");
        scanf("%d", &choice);

        switch (choice) {
            case 1:
                // Enter Polynomial 1
                // (You can modify this part to read coefficients and exponents from the user)
                insertTerm(&poly1, 5, 2);
                insertTerm(&poly1, 3, 1);
                insertTerm(&poly1, 1, 0);
                break;

            case 2:
                // Enter Polynomial 2
                // (You can modify this part to read coefficients and exponents from the user)
                insertTerm(&poly2, 2, 3);
                insertTerm(&poly2, -1, 2);
                insertTerm(&poly2, 4, 0);
                break;

            case 3:
                // Add Polynomials
                {
                    Node* sum = addPolynomials(poly1, poly2);
                    printf("Sum: ");
                    displayPolynomial(sum);
                    freePolynomial(sum);
                }
                break;

            case 4:
                // Subtract Polynomials
                {
                    Node* difference = subtractPolynomials(poly1, poly2);
                    printf("Difference: ");
                    displayPolynomial(difference);
                    freePolynomial(difference);
                }
                break;

            case 5:
                // Display Polynomials
                printf("Polynomial 1: ");
                displayPolynomial(poly1);
                printf("Polynomial 2: ");
                displayPolynomial(poly2);
                break;

            case 6:
                // Quit
                break;

            default:
                printf("Invalid choice. Please enter a number between 1 and 6.\\n");
        }

    } while (choice != 6);

    freePolynomial(poly1);
    freePolynomial(poly2);
    return 0;
}

'''

queue_using_ll='''
#include <stdio.h>
#include <stdlib.h>

// Define the structure for a node in the linked list
struct Node {
    int data;
    struct Node* next;
};

// Define the structure for the queue
struct Queue {
    struct Node* front;
    struct Node* rear;
};

// Function to create a new node
struct Node* createNode(int value) {
    struct Node* newNode = (struct Node*)malloc(sizeof(struct Node));
    newNode->data = value;
    newNode->next = NULL;
    return newNode;
}

// Function to initialize an empty queue
struct Queue* createQueue() {
    struct Queue* queue = (struct Queue*)malloc(sizeof(struct Queue));
    queue->front = queue->rear = NULL;
    return queue;
}

// Function to enqueue a value into the queue
void enqueue(struct Queue* queue, int value) {
    struct Node* newNode = createNode(value);
    if (queue->rear == NULL) {
        queue->front = queue->rear = newNode;
    } else {
        queue->rear->next = newNode;
        queue->rear = newNode;
    }
    printf("%d enqueued to the queue.\\n", value);
}

// Function to dequeue a value from the queue
int dequeue(struct Queue* queue) {
    if (queue->front == NULL) {
        printf("Queue underflow.\\n");
        return -1;
    }

    struct Node* temp = queue->front;
    int dequeuedValue = temp->data;

    queue->front = queue->front->next;
    if (queue->front == NULL) {
        queue->rear = NULL; // Reset rear when the last element is dequeued
    }

    free(temp);
    return dequeuedValue;
}

// Function to display the elements of the queue
void display(struct Queue* queue) {
    if (queue->front == NULL) {
        printf("Queue is empty.\\n");
        return;
    }

    printf("Queue elements: ");
    struct Node* current = queue->front;
    while (current != NULL) {
        printf("%d ", current->data);
        current = current->next;
    }
    printf("\\n");
}

int main() {
    struct Queue* queue = createQueue();
    int choice, value;

    do {
        // Display menu
        printf("\\nMenu:\\n");
        printf("1. Enqueue\\n");
        printf("2. Dequeue\\n");
        printf("3. Display\\n");
        printf("4. Exit\\n");
        printf("Enter your choice: ");
        scanf("%d", &choice);

        switch (choice) {
            case 1:
                printf("Enter the value to enqueue: ");
                scanf("%d", &value);
                enqueue(queue, value);
                break;
            case 2:
                value = dequeue(queue);
                if (value != -1) {
                    printf("Dequeued value: %d\\n", value);
                }
                break;
            case 3:
                display(queue);
                break;
            case 4:
                printf("Exiting the program.\\n");
                break;
            default:
                printf("Invalid choice. Please try again.\\n");
        }

    } while (choice != 4);

    // Free the memory allocated for the queue
    while (queue->front != NULL) {
        struct Node* temp = queue->front;
        queue->front = queue->front->next;
        free(temp);
    }

    free(queue);

    return 0;
}

'''

stack_using_ll='''
#include <stdio.h>
#include <stdlib.h>

// Define the structure for a node in the linked list
struct Node {
    int data;
    struct Node* next;
};

// Function to create a new node
struct Node* createNode(int value) {
    struct Node* newNode = (struct Node*)malloc(sizeof(struct Node));
    newNode->data = value;
    newNode->next = NULL;
    return newNode;
}

// Function to push a value onto the stack
void push(struct Node** top, int value) {
    struct Node* newNode = createNode(value);
    newNode->next = *top;
    *top = newNode;
    printf("%d pushed to the stack.\\n", value);
}

// Function to pop a value from the stack
int pop(struct Node** top) {
    if (*top == NULL) {
        printf("Stack underflow.\\n");
        return -1;
    }

    struct Node* temp = *top;
    *top = (*top)->next;
    int poppedValue = temp->data;
    free(temp);
    return poppedValue;
}

// Function to display the elements of the stack
void display(struct Node* top) {
    if (top == NULL) {
        printf("Stack is empty.\\n");
        return;
    }

    printf("Stack elements: ");
    while (top != NULL) {
        printf("%d ", top->data);
        top = top->next;
    }
    printf("\\n");
}

int main() {
    struct Node* top = NULL;
    int choice, value;

    do {
        // Display menu
        printf("\\nMenu:\\n");
        printf("1. Push\\n");
        printf("2. Pop\\n");
        printf("3. Display\\n");
        printf("4. Exit\\n");
        printf("Enter your choice: ");
        scanf("%d", &choice);

        switch (choice) {
            case 1:
                printf("Enter the value to push: ");
                scanf("%d", &value);
                push(&top, value);
                break;
            case 2:
                value = pop(&top);
                if (value != -1) {
                    printf("Popped value: %d\\n", value);
                }
                break;
            case 3:
                display(top);
                break;
            case 4:
                printf("Exiting the program.\\n");
                break;
            default:
                printf("Invalid choice. Please try again.\\n");
        }

    } while (choice != 4);

    // Free the memory allocated for the stack
    while (top != NULL) {
        struct Node* temp = top;
        top = top->next;
        free(temp);
    }

    return 0;
}

'''

infix_to_postfix='''
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

int isOperator(char ch) {
    return (ch == '+' || ch == '-' || ch == '*' || ch == '/' || ch == '%');
}

int hasHigherPrecedence(char op1, char op2) {
    if ((op1 == '+' || op1 == '-') && (op2 == '*' || op2 == '/' || op2 == '%'))
        return 0;
    return 1;
}

void infixToPostfix(char infix[], char postfix[]) {
    int length = strlen(infix);
    char stack[length];
    int top = -1;
    int outputIndex = 0;

    for (int i = 0; i < length; i++) {
        char ch = infix[i];

        if (ch == ' ')
            continue;

        if (isOperator(ch)) {
            while (top >= 0 && stack[top] != '(' && hasHigherPrecedence(stack[top], ch)) {
                postfix[outputIndex++] = stack[top--];
            }
            stack[++top] = ch;
        } else if (ch == ')') {
            while (top >= 0 && stack[top] != '(') {
                postfix[outputIndex++] = stack[top--];
            }
            if (top >= 0) {
                top--;
            }
        } else if (ch == '(') {
            stack[++top] = ch;
        } else {
            postfix[outputIndex++] = ch;
        }
    }

    while (top >= 0) {
        postfix[outputIndex++] = stack[top--];
    }

    postfix[outputIndex] = '\0';
}

int evaluatePostfix(char postfix[]) {
    int length = strlen(postfix);
    int stack[length];
    int top = -1;

    for (int i = 0; i < length; i++) {
        char ch = postfix[i];

        if (isdigit(ch)) {
            stack[++top] = ch - '0';
        } else if (isOperator(ch)) {
            int operand2 = stack[top--];
            int operand1 = stack[top--];

            switch (ch) {
                case '+':
                    stack[++top] = operand1 + operand2;
                    break;
                case '-':
                    stack[++top] = operand1 - operand2;
                    break;
                case '*':
                    stack[++top] = operand1 * operand2;
                    break;
                case '/':
                    stack[++top] = operand1 / operand2;
                    break;
                case '%':
                    stack[++top] = operand1 % operand2;
                    break;
            }
        }\n
    }

    return stack[top];
}

int main() {
    char infix[100], postfix[100];
    int choice;

    do {
        printf("\\nMenu:\\n");
        printf("1. Convert infix to postfix\\n");
        printf("2. Evaluate postfix expression\\n");
        printf("3. Exit\\n");
        printf("Enter your choice: ");
        scanf("%d", &choice);

        switch (choice) {
            case 1:
                printf("Enter an infix expression: ");
                getchar(); // Consume the newline character left in the buffer
                gets(infix);
                infixToPostfix(infix, postfix);
                printf("Postfix expression: %%s\\n", postfix);
                break;
            case 2:
                printf("Enter a postfix expression: ");
                getchar();
                gets(postfix);
                printf("Result of evaluation: %d\\n", evaluatePostfix(postfix));
                break;
            case 3:
                printf("Exiting the program\\n");
                break;
            default:
                printf("Invalid choice. Please enter a valid option.\\n");
        }

    } while (choice != 3);

    return 0;
}

'''

double_queue='''
#include <stdio.h>
#define SIZE 5

int queue[SIZE], front = -1, rear = -1;

void enqueue_front() {
    if (rear == SIZE - 1) {
        printf("Queue overflow\\n");
        return;
    }
    int data;
    printf("Enter data to be entered: ");
    scanf("%d", &data);
    if (front == -1) {
        front = rear = 0;
        queue[front] = data;
    } else {
        for (int i = rear; i >= front; i--) {
            queue[i + 1] = queue[i];
        }
        rear++;
        queue[front] = data;
    }
    printf("%d added to queue\\n", data);
}

void enqueue_rear() {
    if (rear == SIZE - 1) {
        printf("Queue overflow\\n");
        return;
    }
    int data;
    printf("Enter data to be entered: ");
    scanf("%d", &data);
    if (front == -1) {
        front = 0;
    }
    rear++;
    queue[rear] = data;
    printf("%d added to queue\\n", data);
}

void dequeue_front() {
    if (front == -1) {
        printf("Queue underflow\\n");
        return;
    }
    printf("%d removed from queue\\n", queue[front]);
    front++;
    if (front > rear) {
        front = rear = -1;
    }
}

void dequeue_rear() {
    if (rear == -1) {
        printf("Queue underflow\\n");
        return;
    }
    printf("%d removed from queue\\n", queue[rear]);
    rear--;
    if (front > rear) {
        front = rear = -1;
    }
}

void display() {
    if (front == -1) {
        printf("Queue is empty\\n");
    } else {
        printf("Queue elements are:\\n");
        for (int i = front; i <= rear; i++) {
            printf("Position %d, Element %d\\n", i, queue[i]);
        }
    }
}

int main() {
    int choice;
    do {
        printf("1. Enqueue Front\\n");
        printf("2. Enqueue Rear\\n");
        printf("3. Dequeue Front\\n");
        printf("4. Dequeue Rear\\n");
        printf("5. Display\\n");
        printf("6. Exit\\n");
        printf("Enter your choice: ");
        scanf("%d", &choice);
        switch (choice) {
            case 1:
                enqueue_front();
                break;
            case 2:
                enqueue_rear();
                break;
            case 3:
                dequeue_front();
                break;
            case 4:
                dequeue_rear();
                break;
            case 5:
                display();
                break;
            case 6:
                printf("Program Terminated.\\n");
                break;
            default:
                printf("Invalid choice.\\n");
        }
    } while (choice != 6);
}

'''

binary_search_tree='''
#include <stdio.h>
#include <stdlib.h>

struct Node {
    int data;
    struct Node *left;
    struct Node *right;
};

struct Node *createNode(int data) {
    struct Node *newNode = (struct Node *)malloc(sizeof(struct Node));
    newNode->data = data;
    newNode->left = newNode->right = NULL;
    return newNode;
}

struct Node *insertNode(struct Node *root, int data) {
    if (root == NULL) {
        return createNode(data);
    }

    if (data < root->data) {
        root->left = insertNode(root->left, data);
    } else if (data > root->data) {
        root->right = insertNode(root->right, data);
    }

    return root;
}


struct Node *findMin(struct Node *root) {
    while (root->left != NULL) {
        root = root->left;
    }
    return root;
}


struct Node *deleteNode(struct Node *root, int data) {
    if (root == NULL) {
        return root;
    }

    if (data < root->data) {
        root->left = deleteNode(root->left, data);
    } else if (data > root->data) {
        root->right = deleteNode(root->right, data);
    } else {
        
        if (root->left == NULL) {
            struct Node *temp = root->right;
            free(root);
            return temp;
        } else if (root->right == NULL) {
            struct Node *temp = root->left;
            free(root);
            return temp;
        }

        struct Node *temp = findMin(root->right);

        root->data = temp->data;

        root->right = deleteNode(root->right, temp->data);
    }
    return root;
}


struct Node *searchNode(struct Node *root, int data) {
    if (root == NULL || root->data == data) {
        return root;
    }

    if (data < root->data) {
        return searchNode(root->left, data);
    } else {
        return searchNode(root->right, data);
    }
}

void inorderTraversal(struct Node *root) {
    if (root != NULL) {
        inorderTraversal(root->left);
        printf("%d ", root->data);
        inorderTraversal(root->right);
    }
}

void postorderTraversal(struct Node *root) {
    if (root != NULL) {
        postorderTraversal(root->left);
        postorderTraversal(root->right);
        printf("%d ", root->data);
    }
}

void preorderTraversal(struct Node *root) {
    if (root != NULL) {
        printf("%d ", root->data);
        preorderTraversal(root->left);
        preorderTraversal(root->right);
    }
}

int main() {
    struct Node *root = NULL;
    int choice, data;

    do {
        printf("\\nBinary Tree Operations:\\n");
        printf("1. Insert\\n");
        printf("2. Delete\\n");
        printf("3. Search\\n");
        printf("4. Display (Inorder Traversal)\\n");
        printf("5. Display (Preorder Traversal)\\n");
        printf("6. Display (Postorder Traversal)\\n");
        printf("7. Exit\\n");

        printf("Enter your choice: ");
        scanf("%d", &choice);

        switch (choice) {
            case 1:
                printf("Enter data to insert: ");
                scanf("%d", &data);
                root = insertNode(root, data);
                break;
            case 2:
                printf("Enter data to delete: ");
                scanf("%d", &data);
                root = deleteNode(root, data);
                break;
            case 3:
                printf("Enter data to search: ");
                scanf("%d", &data);
                if (searchNode(root, data) != NULL) {
                    printf("Node found.\\n");
                } else {
                    printf("Node not found.\\n");
                }
                break;
            case 4:
                printf("Inorder Traversal: ");
                inorderTraversal(root);
                printf("\\n");
                break;
            case 5:
                printf("Preorder Traversal: ");
                preorderTraversal(root);
                printf("\\n");
                break;
            case 6:
                printf("Postorder Traversal: ");
                postorderTraversal(root);
                printf("\\n");
                break;
            case 7:
                printf("Exiting program.\\n");
                break;
            default:
                printf("Invalid choice. Please enter a valid option.\\n");
        }

    } while (choice != 7);

    return 0;
}
'''

graph_bfs_dfs='''
#include <stdio.h>
#include <stdlib.h>

#define NODES 8

int adj[NODES][NODES] = {
    {0, 1, 1, 1, 0, 0, 0, 0},
    {1, 0, 0, 0, 1, 0, 0, 1},
    {1, 0, 0, 0, 1, 0, 0, 0},
    {1, 0, 0, 0, 0, 1, 0, 0},
    {0, 1, 1, 0, 0, 0, 1, 0},
    {0, 0, 0, 1, 0, 0, 1, 0},
    {0, 0, 0, 0, 1, 1, 0, 1},
    {0, 1, 0, 0, 0, 0, 1, 0}
};

int visited[NODES];


void bfs(int start) {
    int queue[NODES];
    int front = -1, rear = -1;

    printf("BFS traversal starting from node %d: ", start);

    visited[start] = 1;
    queue[++rear] = start;

    while (front != rear) {
        int current = queue[++front];
        printf("%c ", 'A' + current);

        for (int i = 0; i < NODES; ++i) {
            if (adj[current][i] == 1 && !visited[i]) {
                visited[i] = 1;
                queue[++rear] = i;
            }
        }
    }

    // Reset visited array for future use
    for (int i = 0; i < NODES; ++i) {
        visited[i] = 0;
    }

    printf("\\n");
}

void dfsRecursive(int node) {
    visited[node] = 1;
    printf("%c ", 'A' + node);

    for (int i = 0; i < NODES; ++i) {
        if (adj[node][i] == 1 && !visited[i]) {
            dfsRecursive(i);
        }
    }
}

void dfs(int start) {
    printf("DFS traversal starting from node %d: ", start);
    dfsRecursive(start);

    // Reset visited array for future use
    for (int i = 0; i < NODES; ++i) {
        visited[i] = 0;
    }

    printf("\\n");
}

int main() {
    int choice, start;

    do {
        printf("\\nMenu:\\n");
        printf("1. Breadth-First Search (BFS)\\n");
        printf("2. Depth-First Search (DFS)\\n");
        printf("3. Exit\\n");
        printf("Enter your choice: ");
        scanf("%d", &choice);

        switch (choice) {
            case 1:
                printf("Enter the starting node for BFS: ");
                scanf("%d", &start);
                bfs(start);
                break;
            case 2:
                printf("Enter the starting node for DFS: ");
                scanf("%d", &start);
                dfs(start);
                break;
            case 3:
                printf("Exiting the program.\\n");
                break;
            default:
                printf("Invalid choice. Please enter a valid option.\\n");
        }
    } while (choice != 3);

    return 0;
}

'''

binary_search='''
#include <stdio.h>
#include <conio.h>

int binarySearch(int arr[], int n, int data) {
    int left = 0;
    int right = n - 1;

    while (left <= right) {
        int mid = left + (right - left) / 2;

        if (arr[mid] == data) {
            return mid; 
        } else if (arr[mid] < data) {
            left = mid + 1; 
        } else {
            right = mid - 1; 
        }
    }

    return -1; 
}

int main() {
    int arr[10], n, i, data;

    printf("Enter the number of elements: ");
    scanf("%d", &n);

    printf("Enter the elements (in ascending order):\\n");
    for (i = 0; i < n; i++)
        scanf("%d", &arr[i]);

    printf("Enter the element to be searched: ");
    scanf("%d", &data);

    int result = binarySearch(arr, n, data);

    if (result != -1)
        printf("%d found at position %d\\n", data, result + 1);
    else
        printf("%d not found\\n", data);

    return 0;
}

'''

fibonacci_search='''
#include <stdio.h>
#include <conio.h>

int fibonnaciSearch(int arr[], int n, int data) {
    int fib2 = 0;
    int fib1 = 1;
    int fib = fib2 + fib1;

    while (fib < n) {
        fib2 = fib1;
        fib1 = fib;
        fib = fib2 + fib1;
    }

    int offset = -1;

    while (fib > 1) {
        int i = (offset + fib2) < (n - 1) ? (offset + fib2) : (n - 1);

        if (arr[i] < data) {
            fib = fib1;
            fib1 = fib2;
            fib2 = fib - fib1;
            offset = i;
        } else if (arr[i] > data) {
            fib = fib2;
            fib1 = fib1 - fib2;
            fib2 = fib - fib1;
        } else {
            return i;
        }
    }

    if (fib1 && arr[offset + 1] == data) {
        return offset + 1;
    }

    return -1;
}

int main() {
    int arr[10], n, i, data;

    printf("Enter the number of elements: ");
    scanf("%d", &n);

    printf("Enter the elements (in ascending order):\\n");
    for (i = 0; i < n; i++)
        scanf("%d", &arr[i]);

    printf("Enter the element to be searched: ");
    scanf("%d", &data);

    int result = fibonnaciSearch(arr, n, data);

    if (result != -1)
        printf("%d found at position %d\\n", data, result + 1);
    else
        printf("%d not found\\n", data);

    return 0;
}

'''

merge_sort='''
#include <stdio.h>

void merge(int arr[], int l, int m, int r) {
    int i, j, k;
    int n1 = m - l + 1;
    int n2 = r - m;

    int L[n1], R[n2];

    for (i = 0; i < n1; i++)
        L[i] = arr[l + i];
    for (j = 0; j < n2; j++)
        R[j] = arr[m + 1 + j];

    i = 0;
    j = 0;
    k = l;

    while (i < n1 && j < n2) {
        if (L[i] <= R[j]) {
            arr[k] = L[i];
            i++;
        } else {
            arr[k] = R[j];
            j++;
        }
        k++;
    }

    while (i < n1) {
        arr[k] = L[i];
        i++;
        k++;
    }

    while (j < n2) {
        arr[k] = R[j];
        j++;
        k++;
    }
}

void mergeSort(int arr[], int l, int r) {
    if (l < r) {
        int m = l + (r - l) / 2;

        mergeSort(arr, l, m);
        mergeSort(arr, m + 1, r);

        merge(arr, l, m, r);
    }
}

void printArray(int A[], int size) {
    int i;
    for (i = 0; i < size; i++)
        printf("%d ", A[i]);
    printf("\\n");
}

int main() {
    int arr[10], n, i;
    printf("Enter the number of elements: ");
    scanf("%d", &n);

    printf("Enter the elements:\\n");
    for (i = 0; i < n; i++)
        scanf("%d", &arr[i]);

    printf("Original array: ");
    printArray(arr, n);

    mergeSort(arr, 0, n - 1);

    printf("Sorted array: ");
    printArray(arr, n);

    return 0;
}

'''

quick_sort='''
#include <stdio.h>

void swap(int* a, int* b) {
    int t = *a;
    *a = *b;
    *b = t;
}

int partition(int arr[], int low, int high) {
    int pivot = arr[high];
    int i = (low - 1);

    for (int j = low; j <= high - 1; j++) {
        if (arr[j] < pivot) {
            i++;
            swap(&arr[i], &arr[j]);
        }
    }
    swap(&arr[i + 1], &arr[high]);
    return (i + 1);
}

void quickSort(int arr[], int low, int high) {
    if (low < high) {
        int pi = partition(arr, low, high);

        quickSort(arr, low, pi - 1);
        quickSort(arr, pi + 1, high);
    }
}

void printArray(int arr[], int size) {
    for (int i = 0; i < size; i++)
        printf("%d ", arr[i]);
    printf("\\n");
}

int main() {
    int arr[10], n, i;
    printf("Enter the number of elements: ");
    scanf("%d", &n);

    printf("Enter the elements:\\n");
    for (i = 0; i < n; i++)
        scanf("%d", &arr[i]);

    printf("Original array: ");
    printArray(arr, n);

    quickSort(arr, 0, n - 1);

    printf("Sorted array: ");
    printArray(arr, n);

    return 0;
}

'''

selection_sort='''
#include<stdio.h>
#include<conio.h>

void printArray(int a[], int n){
    int i;
    for(i = 0; i < n; i++){
        printf("%d ", a[i]);
    }
    printf("\\n");
}

void selectionSort(int a[], int n){
    int i, j, minIndex, temp;
    for(i = 0; i < n-1; i++){
        minIndex = i;
        for(j = i+1; j < n; j++){
            if(a[j] < a[minIndex]){
                minIndex = j;
            }
        }
        temp = a[i];
        a[i] = a[minIndex];
        a[minIndex] = temp;
    }
}

int main()
{
    int a[10], n, i;
    printf("Enter the number of elements: ");
    scanf("%d", &n);

    printf("Enter the elements :\\n");
    for (i = 0; i < n; i++)
        scanf("%d", &a[i]);

    printArray(a, n);
    selectionSort(a, n);
    printArray(a, n);
    return 0;
}
'''

hashing = '''
#include <stdio.h>
#include<stdlib.h>
#define TABLE_SIZE 10

int h[TABLE_SIZE] = {NULL};

void insert() {
 int key, index, i, hashingKey;
 printf("\\nEnter data:\\n");
 scanf("%d", &key);
 hashingKey = key % TABLE_SIZE;
 for(i = 0; i < TABLE_SIZE; i++)
    {
     index = (hashingKey + i) % TABLE_SIZE;
     if(h[index] == NULL)
     {
        h[index] = key;
         break;
     }
    }

    if(i == TABLE_SIZE)
    {
     printf("\\nelement cannot be inserted\\n");
    }
}

void search() {
 int key, index, i, hashingKey;
 printf("\\nEnter element to be searched:\\n");
 scanf("%d", &key);
 hashingKey = key % TABLE_SIZE;
 for(i = 0; i< TABLE_SIZE; i++)
 {
    index=(hashingKey + i) % TABLE_SIZE;
    if(h[index] == key) {
      printf("Value at index %d", index);
      break;
    }
  }
  if(i == TABLE_SIZE)
    printf("\\n Value Not Found\\n");
}

void display() {
  int i;
  printf("\\nElements are \\n");
  for(i = 0; i < TABLE_SIZE; i++)
    printf("\\nIndex %d value =  %d", i, h[i]);
}

int main()
{
    int opt;
    while(1)
    {
        printf("\\nMenu:\\n1.Insert\\n2.Display\\n3.Search\\n4.Exit \\n");
        scanf("%d", &opt);
        switch(opt)
        {
            case 1:
                insert();
                break;
            case 2:
                display();
                break;
            case 3:
                search();
                break;
            case 4:exit(0);
            default:
            printf("Invalid");
        }
    }
    return 0;
}
'''

circular_queue='''
// Menu-driven program to implement circular queue using array
#include <stdio.h>
#include <conio.h>
#define SIZE 5

int queue[SIZE];
int front = -1, rear = -1;

void enqueue(int val) {
	if (front == (rear + 1) % SIZE) {
		printf("Queue is full!");
	}
	else {
		if (rear == -1)
			front++;
		rear = (rear + 1) % SIZE;
		queue[rear] = val;
	}
}

int dequeue() {
	int x = -1;
	if (front == -1) {
		printf("Queue is empty!");
	}
	else {
		x = queue[front];
		if (front == rear)
			front = rear = -1;
		else
			front = (front + 1) % SIZE;
	}
	return x;
}

void display() {
	int i = front;
	while (i != rear) {
		printf("%d ", queue[i]);
		i = (i + 1) % SIZE;
	}
	printf("%d", queue[i]);
}

int main() {
	int choice, val;
	do {
		printf("\\n1. Enqueue\\n2. Dequeue\\n3. Display\\n4. Exit\\nEnter your choice: ");
		scanf("%d", &choice);
		switch (choice) {
		case 1:
			printf("Enter the value you want to enqueue: ");
			scanf("%d", &val);
			enqueue(val);
			break;
		case 2:
			printf("The value dequeued is: %d", dequeue());
			break;
		case 3:
			display();
			break;
		case 4:
			break;
		default:
			printf("Invalid choice!");
			choice = 4;
			break;
		} 
	} while (choice != 4);

	return 0;
}
'''

insertion_sort='''
#include <stdio.h>

void insertionSort(int arr[], int n) {
    int i, key, j;
    for (i = 1; i < n; i++) {
        key = arr[i];
        j = i - 1;
        while (j >= 0 && arr[j] > key) {
            arr[j + 1] = arr[j];
            j = j - 1;
        }
        arr[j + 1] = key;
    }
}

void printArray(int arr[], int size) {
    int i;
    for (i = 0; i < size; i++)
        printf("%d ", arr[i]);
    printf("\\n");
}

int main() {
    int arr[10], n, i;
    printf("Enter the number of elements: ");
    scanf("%d", &n);

    printf("Enter the elements:\\n");
    for (i = 0; i < n; i++)
        scanf("%d", &arr[i]);

    printf("Original array: ");
    printArray(arr, n);

    insertionSort(arr, n);

    printf("Sorted array: ");
    printArray(arr, n);

    return 0;
}

'''

bubble_sort='''
#include <stdio.h>

void bubbleSort(int arr[], int n) {
    int i, j;
    for (i = 0; i < n - 1; i++) {
        // Last i elements are already in place
        for (j = 0; j < n - i - 1; j++) {
            // Traverse the array from 0 to n-i-1
            // Swap if the element found is greater than the next element
            if (arr[j] > arr[j + 1]) {
                // Swap arr[j] and arr[j + 1]
                int temp = arr[j];
                arr[j] = arr[j + 1];
                arr[j + 1] = temp;
            }
        }
    }
}

void printArray(int arr[], int size) {
    int i;
    for (i = 0; i < size; i++)
        printf("%d ", arr[i]);
    printf("\\n");
}

int main() {
    int arr[10], n, i;
    printf("Enter the number of elements: ");
    scanf("%d", &n);

    printf("Enter the elements:\\n");
    for (i = 0; i < n; i++)
        scanf("%d", &arr[i]);

    printf("Original array: ");
    printArray(arr, n);

    bubbleSort(arr, n);

    printf("Sorted array: ");
    printArray(arr, n);

    return 0;
}

'''

radix_sort='''
#include<stdio.h>
#include<conio.h>

void printArray(int a[], int n)
{
    int i;
    for(i = 0; i < n; i++)
        printf("%d ", a[i]);
    printf("\n");
}

// Function to find the maximum element in an array
int findMax(int arr[], int n) {
    int max = arr[0];
    for (int i = 1; i < n; i++) {
        if (arr[i] > max) {
            max = arr[i];
        }
    }
    return max;
}

// A utility function to do counting sort of arr[] based on the digit represented by exp.
void countingSort(int arr[], int n, int exp) {
    int output[n];
    int count[10] = {0}; // Assuming decimal digits (base 10)

    for (int i = 0; i < n; i++) {
        count[(arr[i] / exp) % 10]++;
    }

    for (int i = 1; i < 10; i++) {
        count[i] += count[i - 1];
    }

    for (int i = n - 1; i >= 0; i--) {
        output[count[(arr[i] / exp) % 10] - 1] = arr[i];
        count[(arr[i] / exp) % 10]--;
    }

    for (int i = 0; i < n; i++) {
        arr[i] = output[i];
    }
}

// Main Radix Sort function
void radixSort(int arr[], int n) {
    int max = findMax(arr, n);

    for (int exp = 1; max / exp > 0; exp *= 10) {
        countingSort(arr, n, exp);
    }
}

int main()
{
    int a[10];
    int n;
    printf("Enter the number of elements: ");
    scanf("%d", &n);

    printf("Enter the elements:\\n");
    for (int i = 0; i < n; i++)
        scanf("%d", &a[i]);

    printf("Original array: ");
    printArray(a, n);

    radixSort(a, n);
    printf("Sorted array: ");

    printArray(a, n);
    return 0;
}
'''

linear_search='''
#include<stdio.h>
#include<conio.h>

int main()
{
    int arr[10], n, i, data, found = 0;

    printf("Enter the number of elements: ");
    scanf("%d", &n);

    printf("Enter the elements:\\n");
    for (i = 0; i < n; i++)
        scanf("%d", &arr[i]);

    printf("Enter the element to be searched: ");
    scanf("%d", &data);

    for (i = 0; i < n; i++)
    {
        if (arr[i] == data)
        {
            found = 1;
            break;
        }
    }

    if (found == 1)
        printf("%d found at position %d\\n", data, i + 1);
    else
        printf("%d not found\\n", data);

    return 0;
}
'''

infix_to_prefix='''
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

int isOperator(char ch) {
    return (ch == '+' || ch == '-' || ch == '*' || ch == '/');
}

int hasHigherPrecedence(char op1, char op2) {
    if ((op1 == '+' || op1 == '-') && (op2 == '*' || op2 == '/'))
        return 0;
    return 1;
}

void infixToPrefix(char infix[], char prefix[]) {
    int length = strlen(infix);
    char stack[length];
    int top = -1;
    int outputIndex = 0;

    
    strrev(infix);

    for (int i = 0; i < length; i++) {
        char ch = infix[i];

        if (ch == ' ')
            continue;

        if (isOperator(ch)) {
            while (top >= 0 && stack[top] != '(' && hasHigherPrecedence(stack[top], ch)) {
                prefix[outputIndex++] = stack[top--];
            }
            stack[++top] = ch;
        } else if (ch == ')') {
            stack[++top] = ch;
        } else if (ch == '(') {
            while (top >= 0 && stack[top] != ')') {
                prefix[outputIndex++] = stack[top--];
            }
            if (top >= 0) {
                top--; 
            }
        } else {
            
            prefix[outputIndex++] = ch;
        }
    }

    
    while (top >= 0) {
        prefix[outputIndex++] = stack[top--];
    }

    prefix[outputIndex] = '\\0';
    
    strrev(prefix);
}

int main() {
    char infix[100], prefix[100];
    
    printf("Enter an infix expression: ");
    gets(infix);

    infixToPrefix(infix, prefix);

    printf("Prefix expression: %s\\n", prefix);

    return 0;
}


'''

doubly_ll='''
#include <stdio.h>
#include <stdlib.h>

struct Node {
    int data;
    struct Node* next;
    struct Node* prev;
};

void insert(struct Node** head, int data) {
    struct Node* newNode = (struct Node*)malloc(sizeof(struct Node));
    newNode->data = data;
    newNode->next = NULL;
    newNode->prev = NULL;

    if (*head == NULL) {
        *head = newNode;
    } else {
        struct Node* current = *head;
        while (current->next != NULL) {
            current = current->next;
        }
        current->next = newNode;
        newNode->prev = current;
    }
}

void removeNode(struct Node** head, int data) {
    struct Node* current = *head;

    while (current != NULL && current->data != data) {
        current = current->next;
    }

    if (current == NULL) {
        printf("Element not found in the list.\\n");
        return;
    }

    if (current->prev != NULL) {
        current->prev->next = current->next;
    } else {
        *head = current->next;
    }

    if (current->next != NULL) {
        current->next->prev = current->prev;
    }

    free(current);
}

void display(struct Node* head) {
    struct Node* current = head;

    if (current == NULL) {
        printf("The list is empty.\\n");
        return;
    }

    printf("Doubly Linked List: ");
    while (current != NULL) {
        printf("%d -> ", current->data);
        current = current->next;
    }
    printf("NULL\\n");
}

int search(struct Node* head, int data) {
    struct Node* current = head;
    int position = 1;

    while (current != NULL) {
        if (current->data == data) {
            return position;
        }
        current = current->next;
        position++;
    }

    return -1;
}

int main() {
    struct Node* head = NULL;
    int choice, data;

    while (1) {
        printf("\\nDoubly Linked List Operations:\\n");
        printf("1. Insert\\n");
        printf("2. Remove\\n");
        printf("3. Display\\n");
        printf("4. Search\\n");
        printf("5. Exit\\n");
        printf("Enter your choice: ");
        scanf("%d", &choice);

        switch (choice) {
            case 1:
                printf("Enter data to insert: ");
                scanf("%d", &data);
                insert(&head, data);
                break;
            case 2:
                printf("Enter data to remove: ");
                scanf("%d", &data);
                removeNode(&head, data);
                break;
            case 3:
                display(head);
                break;
            case 4:
                printf("Enter data to search: ");
                scanf("%d", &data);
                int position = search(head, data);
                if (position != -1) {
                    printf("Element found at position %d.\\n", position);
                } else {
                    printf("Element not found in the list.\\n");
                }
                break;
            case 5:
                exit(0);
            default:
                printf("Invalid choice. Please try again.\\n");
        }
    }

    return 0;
}

'''

balanced_paranthesis='''
#include <stdio.h>

#define SIZE 100
char stack[SIZE];
int top = -1;

void push(char val) {
    if (top == SIZE - 1) {
        printf("\\nStack overflow!\\n");
    } else {
        top++;
        stack[top] = val;
    }
}

char pop() {
    char x = -1;
    if (top == -1) {
        printf("\\nStack underflow\\n");
    } else {
        x = stack[top];
        top--;
    }
    return x;
}

char peek() {
    char x = -1;
    if (top == -1) {
        printf("\\nStack underflow\\n");
    } else {
        x = stack[top];
    }
    return x;
}

void display() {
    int i;
    if (top == -1)
        printf("\\nStack is empty\\n");
    else {
        for (i = top; i >= 0; i--) {
            printf("%c ", stack[i]);
        }
        printf("\\n");
    }
}

int main() {
    char expression[SIZE];
    printf("Enter an expression: ");
    fgets(expression, SIZE, stdin);
    for (int i = 0; expression[i] != '\\0'; i++) {
        if (expression[i] == '(') {
            push(expression[i]);
        } else if (expression[i] == ')') {
            if (peek() == '(') {
                pop();
            } else {
                printf("Invalid expression!\\n");
                break;
            }
        }
    }
    if (top == -1) {
        printf("Valid expression!\\n");
    } else {
        printf("Invalid expression!\\n");
    }
    return 0;
}

'''

multi_balanced_paranthesis='''
#include <stdio.h>

#define SIZE 100
char stack[SIZE];
int top = -1;

void push(char val) {
    if (top == SIZE - 1) {
        printf("\\nStack overflow!\\n");
    } else {
        top++;
        stack[top] = val;
    }
}

char pop() {
    char x = -1;
    if (top == -1) {
        printf("\\nStack underflow\\n");
    } else {
        x = stack[top];
        top--;
    }
    return x;
}

char peek() {
    char x = -1;
    if (top == -1) {
        printf("\\nStack underflow\\n");
    } else {
        x = stack[top];
    }
    return x;
}

void display() {
    int i;
    if (top == -1)
        printf("\\nStack is empty\\n");
    else {
        for (i = top; i >= 0; i--) {
            printf("%c ", stack[i]);
        }
        printf("\\n");
    }
}

int main() {
    char expression[SIZE];
    printf("Enter an expression: ");
    fgets(expression, SIZE, stdin);
    for (int i = 0; expression[i] != '\\0'; i++) {
        if (expression[i] == '(' || expression[i] == '{' || expression[i] == '[') {
            push(expression[i]);
        } else if (expression[i] == ')') {
            if (peek() == '(') {
                pop();
            } else {
                break;
            }
        } else if (expression[i] == '}') {
            if (peek() == '{') {
                pop();
            } else {
                break;
            }
        } else if (expression[i] == ']') {
            if (peek() == '[') {
                pop();
            } else {
                break;
            }
        }
    }
    if (top == -1) {
        printf("Valid expression!\\n");
    } else {
        printf("Invalid expression!\\n");
    }
    return 0;
}

'''

priority_queue='''
#include <stdio.h>
#define max 5

struct node{
    int data;
    int priority;
}pq[max];

int rear=-1;

int higestPriority(){
    int p =-1 ;
    for(int i=0; i<=rear; i++){
        p = pq[i].priority>p?pq[i].priority:p;
    }
    return p;
}

void enque(){
    if(rear == max-1){
        printf("Full");
        return;
    }
    rear++;
    printf("Enter data : ");
    scanf("%d", &pq[rear].data);
    printf("Enter Priority : ");
    scanf("%d", &pq[rear].priority);
}

void deque(){
    int i;
    if(rear==-1){
        printf("Empty");
        return;
    }
    int p = higestPriority(), data;
    for(i=0; i<=rear; i++){
        if(p == pq[i].priority){
            printf("\\nData : %d, Priority : %d", pq[i].data, pq[i].priority);
            break;
        }
    }
    for(int j=i; j<rear; j++){
        pq[j].data = pq[j+1].data;
        pq[j].priority = pq[j+1].priority;
    }
    rear--;
}

void display(){
    if(rear==-1){
        printf("Empty");
        return;
    }
    for(int i=0; i<=rear; i++){
        printf("\\nData : %d, Priority : %d", pq[i].data, pq[i].priority);
    }
}

void main(){
    int ch, flag=1;
    while(flag){
        printf("\\n1.Enque \\n2.Deque \\n3.Display \\n4.Exit : ");
        scanf("%d", &ch);
        switch(ch){
            case 1:enque();break;
            case 2:deque();break;
            case 3:display();break;
            case 4:flag=0;break;
        }
    }
}
'''

dsa_exp = {
    'queue_using_array.c': queue_using_array,
    'stack_using_array.c': stack_using_array,
    'linked_list.c': linked_list,
    'polynomial_add_sub.c': polynomial_add_sub,
    'queue_using_ll.c': queue_using_ll,
    'stack_using_ll.c': stack_using_ll,
    'priority_queue.c': priority_queue,
    'doubly_ll.c': doubly_ll,
    'circular_queue.c': circular_queue,
    'infix_to_postfix.c': infix_to_postfix,
    'infix_to_prefix.c': infix_to_prefix,
    'graph_bfs_dfs.c': graph_bfs_dfs,
    'double_queue.c': double_queue,
    'binary_search_tree.c': binary_search_tree,
    'binary_search.c':binary_search,
    'linear_search.c': linear_search,
    'fibonacci_search.c': fibonacci_search,
    'merge_sort.c': merge_sort,
    'insertion_sort.c': insertion_sort,
    'bubble_sort.c': bubble_sort,
    'quick_sort.c': quick_sort,
    'radix_sort.c': radix_sort,
    'selection_sort.c': selection_sort,
    'hashing.c': hashing,
    'balanced_paranthesis':balanced_paranthesis,
    'multi_balanced_paranthesis':multi_balanced_paranthesis,
}

def dsa():
    for filename, content in dsa_exp.items():
        with open(filename, 'w') as file:
            file.write(content)
        print(f"File '{filename}' created successfully.")